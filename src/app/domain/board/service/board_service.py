from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.app.domain.board.crud import board_crud as crud
from src.app.domain.board.schemas import board_schemas as schemas


async def create_board(db: Session, board_request: schemas.BoardCreateRequest):
    board = await crud.create_board(db, board_request)
    if not board:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create board")
    return board