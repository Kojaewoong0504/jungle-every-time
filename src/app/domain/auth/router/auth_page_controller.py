from pathlib import Path
from typing import Annotated

from starlette.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.app.core.database import get_db

from src.app.core.security import get_current_user_from_cookie

from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.templating import Jinja2Templates

router = APIRouter()
template = Jinja2Templates(directory=str(Path(__file__).resolve().parents[4] / "resource" / "templates"))

DB = Annotated[Session, Depends(get_db)]


@router.get("/login")
async def login_page(request: Request):
    return template.TemplateResponse("login.html", {"request": request})


@router.get("/sign-up")
async def sign_up_page(request: Request):
    return template.TemplateResponse("signup.html", {"request": request})



@router.get("/main", response_class=HTMLResponse)
async def main_page(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user_from_cookie(request, db)
    if user:
        return template.TemplateResponse("main.html", {"request": request, "user": user})
    return RedirectResponse("/api/v1/auth/page/login")

