import os
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.app.core.database import get_db
from src.app.domain.auth.schemas import auth_schemas as schemas
from src.app.domain.auth.service import auth_service as service
from src.app.core.security import create_access_token

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse, JSONResponse

router = APIRouter()

DB = Annotated[Session, Depends(get_db)]


@router.post("/sign-up")
async def sign_up(
        response: Response,
        sign_up_request: schemas.UserSignupRequest,
        db: DB
):
    try:
        # 1. 이메일이 있는지(중복 가입) 확인한다.
        await service.check_duplicate_email(db, sign_up_request.email)
        # 2. 회원가입 진행
        await service.join(db, sign_up_request)
        db.commit()
        # 3. 회원가입 성공 시 새로운 acces_token 생성
        access_token = create_access_token(subject=sign_up_request.email)
        # 4. 반환
        # return schemas.TokenResponse(access_token=access_token)
        response.set_cookie(
            key=os.environ.get('ACCESS_TOKEN_KEY', 'access_token'),  # import os
            value=f"Bearer {access_token}",
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24,
            path="/"
        )

        return JSONResponse(
            content={"message": "Signup successful"},
            status_code=200
        )
    except HTTPException as e:
        db.rollback()
        raise
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to signup user: {str(e)}"
        )


@router.post("/login")
async def login(
        db: DB,
        from_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = await service.authenticate_user(db, from_data.username, from_data.password)
        access_token = create_access_token(subject=user.email)
        # return schemas.TokenResponse(access_token=access_token)
        redirect_response = RedirectResponse(url="/api/v1/auth/page/main", status_code=302)
        redirect_response.set_cookie(
            key=os.environ.get('ACCESS_TOKEN_KEY', 'access_token'),  # import os
            value=f"Bearer {access_token}",
            httponly=True,
            secure=False,  # HTTPS 시 True
            samesite="lax",
            max_age=60 * 60 * 24,
            path="/"
        )
        return redirect_response
    except HTTPException as e:
        raise e
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/api/v1/auth/page/login", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response
