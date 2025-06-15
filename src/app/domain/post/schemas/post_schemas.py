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

    model_config = ConfigDict(from_attributes=True)
