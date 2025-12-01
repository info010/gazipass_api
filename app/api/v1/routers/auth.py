from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from api.v1.controllers import auth_controller
from api.v1.validators.auth_models import AuthResponse, LoginRequest, RefreshResponse, RegisterRequest, TokenRequest, UserResponse
from api.v1.validators.common.api_models import APIResponse
from database.database import get_db
from utils.security import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(prefix="/Auth", tags=["Auth"])

@router.get(
    "/me",
    summary="Get current User",
    response_model=APIResponse[UserResponse]
)
async def me(_claims: dict = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await auth_controller.me(_claims["user_id"], _db)

@router.post(
    "/register",
    summary="Register", 
    response_model=APIResponse[AuthResponse]
)
async def register(req: RegisterRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.register(req, _db)

@router.post(
    "/login",
    summary="Login",
    response_model=APIResponse[AuthResponse]
)
async def login(req: LoginRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.login(req, _db)

@router.post(
    "/logout",
    summary="Logout current User",
    response_model=APIResponse[bool]
)
async def logout(req: TokenRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.logout(req, _db)

@router.post(
    "/refresh",
    summary="Refresh token",
    response_model=APIResponse[RefreshResponse]
)
async def refresh(req: TokenRequest, _db: AsyncSession = Depends(get_db)):
    return await auth_controller.refresh(req, _db)