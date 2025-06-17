from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.domain.post.crud import post_like_crud as crud
from src.app.domain.post.schemas import post_like_schemas as schemas


async def toggle_like(db: Session, post_id: int, user_id: int):
    post_like = await crud.toggle_like(db, post_id, user_id)
    if not post_like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post_like


async def get_likes_by_user(db: Session, user_id: int):
    return await crud.get_likes_by_user(db, user_id)


async def get_posts_liked_by_user(db: Session, user_id: int):
    return await crud.get_posts_liked_by_user(db, user_id)
