from typing import Optional
from pydantic import BaseModel, ConfigDict
from src.app.config.config import settings


class UserResponseDto(BaseModel):
    id: int
    email: str
    username: str
    nickname: str

    model_config = {
        "from_attributes": True
    }


class UserRequestDto(BaseModel):
    id: int
    email: str
    username: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)


class UserDto(BaseModel):
    id: int
    email: str
    username: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)