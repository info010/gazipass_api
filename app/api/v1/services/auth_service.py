import base64
import os
from fastapi import HTTPException, status
from api.v1.validators.auth_models import RefreshResponse, RegisterRequest, AuthResponse, UserResponse, LoginRequest, TokenRequest, LogoutResponse
from database.crud.user_crud import get_user_by_email, create_user, verify_users_pwd, get_user_by_id
from database.crud.refresh_token_crud import (
    create_refresh_token,
    get_refresh_token,
    revoke_refresh_token,
    delete_expired_tokens
)
from utils.security import create_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

def _generate_refresh_token() -> str:
    return base64.b64encode(os.urandom(32)).decode("utf-8")

def _generate_access_token(data: dict) -> str:
    return create_jwt(data=data, minutes=5)

# --- REGISTER ---
async def register(req: RegisterRequest, db: AsyncSession) -> AuthResponse:
    exists = await get_user_by_email(db=db, email=req.email)
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )

    new_user = await create_user(
        db=db,
        username=req.username,
        email=req.email,
        password=req.password,
        first_name=req.first_name,
        last_name=req.last_name,
    )

    if not new_user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed."
        )

    access_token = _generate_access_token(data={"user_id": str(new_user.id)})
    refresh_token = _generate_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    await create_refresh_token(db, new_user, refresh_token, expires_at)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


# --- LOGIN ---
async def login(req: LoginRequest, db: AsyncSession) -> AuthResponse:
    user = await verify_users_pwd(db=db, email=req.email, pwd=req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong email or password"
        )

    access_token = _generate_access_token(data={"user_id": str(user.id)})
    refresh_token = _generate_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    await create_refresh_token(db, user, refresh_token, expires_at)

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


# --- ME ---
async def me(user_id: str, db: AsyncSession) -> UserResponse:
    user = await get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return UserResponse(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        roles=user.roles
    )


# --- LOGOUT ---
async def logout(req: TokenRequest, db: AsyncSession) -> LogoutResponse:
    db_token = await get_refresh_token(db, req.refresh_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found."
        )

    await revoke_refresh_token(db, req.refresh_token)
    await delete_expired_tokens(db)

    return LogoutResponse(
        success=True,
        message="Successfully logged out."
    )


# --- REFRESH ---
async def refresh(req: TokenRequest, db: AsyncSession) -> RefreshResponse:
    db_token = await get_refresh_token(db, req.refresh_token)
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found."
        )

    access_token = _generate_access_token(data={"user_id": str(db_token.id)})

    return RefreshResponse(
        success=True,
        message="Token successfully refreshed.",
        access_token=access_token
    )