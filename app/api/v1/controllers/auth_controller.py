from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.services import auth_service
from api.v1.validators.auth_models import AuthResponse, LoginRequest, RefreshResponse, RegisterRequest, TokenRequest, UserResponse
from api.v1.validators.common.api_models import APIResponse

async def register(req: RegisterRequest, _db: AsyncSession) -> APIResponse[AuthResponse]:
    return await auth_service.register(req, _db)

async def login(req: LoginRequest, _db: AsyncSession) -> APIResponse[AuthResponse]:
    return await auth_service.login(req, _db)

async def me(user_id: str, _db: AsyncSession) -> APIResponse[UserResponse]:
    return await auth_service.me(user_id, _db)

async def logout(req: TokenRequest, _db: AsyncSession) -> APIResponse[bool]:
    return await auth_service.logout(req, _db)

async def refresh(req: TokenRequest, _db: AsyncSession) -> APIResponse[RefreshResponse]:
    return await auth_service.refresh(req, _db)