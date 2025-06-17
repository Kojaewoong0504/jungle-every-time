from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommentCreateRequest(BaseModel):
    post_id: int
    comment: str


class CommentResponse(BaseModel):
    id: int
    comment: str
    user_id: int
    posts_id: int
    post_title: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)