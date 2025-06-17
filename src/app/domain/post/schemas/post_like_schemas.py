from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostLikeResponse(BaseModel):
    id: int
    user_id: int
    posts_id: int
    status: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostLikeToggleResponse(PostLikeResponse):
    """Response returned when toggling a like."""
    likes: int