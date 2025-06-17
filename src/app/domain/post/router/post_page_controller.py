from pathlib import Path
from typing import Annotated

from starlette.responses import HTMLResponse
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from src.app.core.database import get_db
from src.app.core.security import get_current_user_from_cookie
from src.app.models.models import User, Board, Post

router = APIRouter()
template = Jinja2Templates(directory=str(Path(__file__).resolve().parents[4] / "resource" / "templates"))

DB = Annotated[Session, Depends(get_db)]


@router.get("/write", response_class=HTMLResponse)
async def write_page(request: Request, db: DB):
    user = await get_current_user_from_cookie(request, db)
    boards = db.query(Board).all()
    if user:
        return template.TemplateResponse(
            "post_write.html",
            {"request": request, "user": user, "boards": boards},
        )
    return RedirectResponse("/api/v1/auth/page/login")


@router.get("/{post_id}", response_class=HTMLResponse)
async def post_detail_page(request: Request, post_id: int, db: DB):
    user = await get_current_user_from_cookie(request, db)
    if not user:
        return RedirectResponse("/api/v1/auth/page/login")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        return RedirectResponse("/api/v1/auth/page/main")
    post.views += 1
    db.commit()
    return template.TemplateResponse(
        "post_detail.html",
        {"request": request, "user": user, "post": post},
    )
