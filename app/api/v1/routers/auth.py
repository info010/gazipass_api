from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from core.common.base_router import BaseRouter

from database.database import get_db
from core.security.auth import get_current_user
from controllers.auth_controller import auth_controller
from validators.auth_models import (
    RegisterRequest, LoginRequest, TokenRequest
)
from core.common.api_models import APIResponse

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = BaseRouter(prefix="/Auth", tags=["Auth"])


@router.get("/me", response_model=APIResponse)
async def me(_claims=Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await auth_controller.with_service(_db).me(_claims["user_id"])


@router.post("/register", response_model=APIResponse)
async def register(req: RegisterRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.with_service(_db).register(req)


@router.post("/login", response_model=APIResponse)
async def login(req: LoginRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.with_service(_db).login(req)


@router.post("/logout", response_model=APIResponse)
async def logout(_claims=Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await auth_controller.with_service(_db).logout(_claims["user_id"])


@router.post("/refresh", response_model=APIResponse)
async def refresh(req: TokenRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.with_service(_db).refresh(req)