from sqlalchemy.orm import Session

from src.app.models.models import Post, Board
from src.app.domain.post.schemas import post_schemas as schemas


async def create_post(db: Session, post_request: schemas.PostCreateRequest, user_id: int) -> Post:
    new_post = Post(
        title=post_request.title,
        content=post_request.content,
        board_id=post_request.board_id,
        user_id=user_id,
    )
    db.add(new_post)
    db.flush()
    return new_post


async def get_posts(db: Session, topic: str | None = None) -> list[Post]:
    query = db.query(Post)
    if topic:
        query = query.join(Board).filter(Board.topic == topic)
    return query.all()
