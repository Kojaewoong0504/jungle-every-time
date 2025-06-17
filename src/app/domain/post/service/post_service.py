from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.app.domain.post.crud import post_crud as crud
from src.app.domain.post.schemas import post_schemas as schemas


async def create_post(db: Session, post_request: schemas.PostCreateRequest, user_id: int):
    post = await crud.create_post(db, post_request, user_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create post")
    return post


async def get_posts(db: Session, topic: str | None = None):
    return await crud.get_posts(db, topic)


async def get_post(db: Session, post_id: int):
    post = await crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    post.views += 1
    return post
