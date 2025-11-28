from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from api.v1.controllers import auth_controller
from api.v1.validators.auth_models import AuthResponse, LoginRequest, LogoutResponse, RefreshResponse, RegisterRequest, TokenRequest, UserResponse
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from utils.security import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(prefix="/Auth", tags=["Auth"])

@router.get(
    "/me",
    summary="Get current User",
    response_model=UserResponse
)
async def me(payload: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await auth_controller.me(payload["user_id"], db)

@router.post(
    "/register",
    summary="Register", 
    response_model=AuthResponse
)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    return await auth_controller.register(req, db)

@router.post(
    "/login",
    summary="Login",
    response_model=AuthResponse
)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    return await auth_controller.login(req, db)

@router.post(
    "/logout",
    summary="Logout current User",
    response_model=LogoutResponse
)
async def logout(req: TokenRequest, db: AsyncSession = Depends(get_db)):
    return await auth_controller.logout(req, db)

@router.post(
    "/refresh",
    summary="Refresh token",
    response_model=RefreshResponse
)
async def refresh(req: TokenRequest, db: AsyncSession = Depends(get_db)):
    return await auth_controller.refresh(req, db)