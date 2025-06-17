from sqlalchemy.orm import Session
from sqlalchemy import select

from src.app.models.models import Comment, Post
from src.app.domain.post.schemas import comment_schemas as schemas


async def create_comment(db: Session, comment_request: schemas.CommentCreateRequest, user_id: int) -> Comment:
    new_comment = Comment(
        comment=comment_request.comment,
        user_id=user_id,
        posts_id=comment_request.post_id,
    )
    db.add(new_comment)
    db.flush()
    return new_comment


async def get_comments_by_post(db: Session, post_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.posts_id == post_id).all()


async def get_comments_by_user(db: Session, user_id: int) -> list[Comment]:
    return db.query(Comment).filter(Comment.user_id == user_id).all()


async def get_posts_commented_by_user(db: Session, user_id: int) -> list[Post]:
    stmt = select(Post).join(Comment).where(Comment.user_id == user_id).distinct()
    return db.scalars(stmt).all()