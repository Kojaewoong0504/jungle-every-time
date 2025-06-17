from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.core.security import get_current_user, get_current_user_from_cookie
from src.app.domain.post.schemas import post_like_schemas as schemas
from src.app.domain.post.service import post_like_service as service
from src.app.domain.post.schemas import post_schemas
from src.app.models.models import User

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]
VALID_USER = Annotated[User, Depends(get_current_user)]
COOKIE_USER = Annotated[User, Depends(get_current_user_from_cookie)]


@router.post("/{post_id}", response_model=schemas.PostLikeToggleResponse)
async def toggle_like(post_id: int, db: DB, current_user: COOKIE_USER) -> schemas.PostLikeToggleResponse:
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        like = await service.toggle_like(db, post_id, current_user.id)
        db.commit()
        return schemas.PostLikeToggleResponse(
            id=like.id,
            user_id=like.user_id,
            posts_id=like.posts_id,
            status=like.status,
            likes=like.post.likes,
            created_at=like.created_at,
        )
    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me", response_model=list[schemas.PostLikeResponse])
async def read_my_likes(db: DB, current_user: COOKIE_USER) -> list[schemas.PostLikeResponse]:
    try:
        likes = await service.get_likes_by_user(db, current_user.id)
        return [schemas.PostLikeResponse.model_validate(l) for l in likes]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/me/posts", response_model=list[post_schemas.PostResponse])
async def read_my_like_posts(db: DB, current_user: COOKIE_USER):
    try:
        posts = await service.get_posts_liked_by_user(db, current_user.id)
        return [post_schemas.PostResponse.model_validate(p) for p in posts]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))