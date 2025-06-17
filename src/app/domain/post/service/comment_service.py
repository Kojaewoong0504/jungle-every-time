from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.domain.post.crud import comment_crud as crud
from src.app.domain.post.schemas import comment_schemas as schemas


async def create_comment(db: Session, comment_request: schemas.CommentCreateRequest, user_id: int):
    comment = await crud.create_comment(db, comment_request, user_id)
    if not comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create comment")
    return comment


async def get_comments_by_post(db: Session, post_id: int):
    return await crud.get_comments_by_post(db, post_id)


async def get_comments_by_user(db: Session, user_id: int):
    return await crud.get_comments_by_user(db, user_id)


async def get_posts_commented_by_user(db: Session, user_id: int):
    return await crud.get_posts_commented_by_user(db, user_id)
