from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.domain.board.schemas import board_schemas as schemas
from src.app.domain.board.service import board_service as service
from src.app.models.models import Board

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=schemas.BoardResponse)
async def create_board(board_request: schemas.BoardCreateRequest, db: DB) -> schemas.BoardResponse:
    try:
        board = await service.create_board(db, board_request)
        db.commit()
        return schemas.BoardResponse.model_validate(board)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[schemas.BoardResponse])
async def read_boards(db: DB) -> list[schemas.BoardResponse]:
    try:
        boards = db.query(Board).all()
        return [schemas.BoardResponse.model_validate(b) for b in boards]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))