from sqlalchemy.orm import Session
from src.app.models.models import PostLike, Post


async def toggle_like(db: Session, post_id: int, user_id: int) -> PostLike | None:
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return None

    post_like = db.query(PostLike).filter(PostLike.posts_id == post_id, PostLike.user_id == user_id).first()
    if post_like:
        post_like.status = not post_like.status
        if post_like.status:
            post.likes += 1
        else:
            if post.likes > 0:
                post.likes -= 1
    else:
        post_like = PostLike(posts_id=post_id, user_id=user_id, status=True)
        db.add(post_like)
        post.likes += 1
    db.flush()
    return post_like


async def get_likes_by_user(db: Session, user_id: int) -> list[PostLike]:
    return db.query(PostLike).filter(PostLike.user_id == user_id, PostLike.status == True).all()


async def get_posts_liked_by_user(db: Session, user_id: int) -> list[Post]:
    return db.query(Post).join(PostLike).filter(PostLike.user_id == user_id, PostLike.status == True).all()