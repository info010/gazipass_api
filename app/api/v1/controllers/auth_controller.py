from api.v1.services import auth_service
from api.v1.validators.auth_models import AuthResponse, LoginRequest, LogoutResponse, RefreshResponse, RegisterRequest, TokenRequest, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

async def register(req: RegisterRequest, db: AsyncSession) -> AuthResponse:
    return await auth_service.register(req, db)

async def login(req: LoginRequest, db: AsyncSession) -> AuthResponse:
    return await auth_service.login(req, db)

async def me(user_id: str, db: AsyncSession) -> UserResponse:
    return await auth_service.me(user_id, db)

async def logout(req: TokenRequest, db: AsyncSession) -> LogoutResponse:
    return await auth_service.logout(req, db)

async def refresh(req: TokenRequest, db: AsyncSession) -> RefreshResponse:
    return await auth_service.refresh(req, db)