from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BoardCreateRequest(BaseModel):
    title: str
    topic: str


class BoardResponse(BaseModel):
    id: int
    title: str
    topic: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)