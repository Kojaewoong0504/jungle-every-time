from sqlalchemy.orm import Session

from src.app.models.models import Board
from src.app.domain.board.schemas import board_schemas as schema


async def create_board(db: Session, board_request: schema.BoardCreateRequest) -> Board:
    new_board = Board(
        title=board_request.title,
        topic=board_request.topic
    )
    db.add(new_board)
    db.flush()
    return new_board
