from fastapi import APIRouter
from .router import auth_controller
from .router import auth_page_controller

router = APIRouter()
router.include_router(auth_controller.router, prefix="/auth", tags=["auth"])
router.include_router(auth_page_controller.router, prefix="/auth/page", tags=["auth/page"])