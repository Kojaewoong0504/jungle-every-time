from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostCreateRequest(BaseModel):
    title: str
    content: str
    board_id: int


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    board_id: int
    user_id: int
    nickname: str | None = None
    likes: int
    views: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
