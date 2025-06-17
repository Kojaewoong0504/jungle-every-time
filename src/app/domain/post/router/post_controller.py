from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.core.security import get_current_user, get_current_user_from_cookie
from src.app.domain.post.schemas import post_schemas as schemas
from src.app.domain.post.service import post_service as service
from src.app.models.models import User

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]
VALID_USER = Annotated[User, Depends(get_current_user)]


@router.post("/", response_model=schemas.PostResponse)
async def create_post(
        post_request: schemas.PostCreateRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_from_cookie),
) -> schemas.PostResponse:
    try:
        post = await service.create_post(db, post_request, current_user.id)
        db.commit()
        return schemas.PostResponse.model_validate(post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[schemas.PostResponse])
async def read_posts(db: DB, topic: str | None = None):
    try:
        posts = await service.get_posts(db, topic)
        return [schemas.PostResponse.model_validate(p) for p in posts]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def read_post(post_id: int, db: DB) -> schemas.PostResponse:
    try:
        post = await service.get_post(db, post_id)
        db.commit()
        return schemas.PostResponse.model_validate(post)
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))