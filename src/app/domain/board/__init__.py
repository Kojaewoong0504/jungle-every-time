from fastapi import APIRouter
from .router import board_controller

router = APIRouter()
router.include_router(board_controller.router, prefix="/board", tags=["board"])