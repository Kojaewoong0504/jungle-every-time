from fastapi import APIRouter
from .router import post_controller, post_page_controller

router = APIRouter()
router.include_router(post_controller.router, prefix="/post", tags=["post"])
router.include_router(post_page_controller.router, prefix="/post/page", tags=["post/page"])