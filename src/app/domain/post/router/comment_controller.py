from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.domain.post.schemas import post_schemas
from src.app.core.security import get_current_user_from_cookie, get_current_user
from src.app.domain.post.schemas import comment_schemas as schemas
from src.app.domain.post.service import comment_service as service
from src.app.models.models import User

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]
VALID_USER = Annotated[User, Depends(get_current_user)]
COOKIE_USER = Annotated[User, Depends(get_current_user_from_cookie)]


@router.post("/", response_model=schemas.CommentResponse)
async def create_comment(comment_request: schemas.CommentCreateRequest, db: DB,
                         current_user: COOKIE_USER) -> schemas.CommentResponse:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        comment = await service.create_comment(db, comment_request, current_user.id)
        db.commit()
        return schemas.CommentResponse.model_validate(comment)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/post/{post_id}", response_model=list[schemas.CommentResponse])
async def read_comments(post_id: int, db: DB) -> list[schemas.CommentResponse]:
    try:
        comments = await service.get_comments_by_post(db, post_id)
        return [schemas.CommentResponse.model_validate(c) for c in comments]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me", response_model=list[schemas.CommentResponse])
async def read_my_comments(db: DB, current_user: COOKIE_USER) -> list[schemas.CommentResponse]:
    try:
        comments = await service.get_comments_by_user(db, current_user.id)
        return [schemas.CommentResponse.model_validate(c) for c in comments]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me/posts", response_model=list[post_schemas.PostResponse])
async def read_posts_commented_me(db: DB, current_user: COOKIE_USER):
    try:
        posts = await service.get_posts_commented_by_user(db, current_user.id)
        return [post_schemas.PostResponse.model_validate(p) for p in posts]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
