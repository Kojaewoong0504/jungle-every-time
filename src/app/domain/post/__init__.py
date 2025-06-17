from fastapi import APIRouter
from .router import post_controller, post_page_controller, comment_controller, post_like_controller

router = APIRouter()
router.include_router(post_controller.router, prefix="/post", tags=["post"])
router.include_router(post_page_controller.router, prefix="/post/page", tags=["post/page"])
router.include_router(comment_controller.router, prefix="/post/comment", tags=["post/comment"])
router.include_router(post_like_controller.router, prefix="/post/like", tags=["post/like"])