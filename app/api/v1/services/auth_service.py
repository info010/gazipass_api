import base64
import os
from fastapi import Depends, HTTPException, status
from core.enums.messages import AuthMessages
from api.v1.validators.common.api_models import APIResponse
from api.v1.validators.auth_models import RefreshResponse, RegisterRequest, AuthResponse, UserResponse, LoginRequest, TokenRequest
from database.crud.user_crud import get_user_by_email, create_user, get_user_by_username, verify_users_pwd, get_user_by_id
from database.crud.refresh_token_crud import (
    create_refresh_token,
    get_refresh_token,
    revoke_refresh_token,
    delete_expired_tokens
)
from utils.security import create_jwt
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

# TODO : Tokenler için yeniden düzenleme gerekmekte

def _generate_refresh_token() -> str:
    return base64.b64encode(os.urandom(32)).decode("utf-8")

def _generate_access_token(data: dict) -> str:
    return create_jwt(data=data, minutes=5)

async def register(req: RegisterRequest, _db: AsyncSession) -> APIResponse[AuthResponse]:
    try:
        email, username = await get_user_by_email(db=_db, email=req.email), await get_user_by_username(db=_db, username=req.username)
        if email or username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= AuthMessages.EMAIL_EXISTS.value
            )
    
        new_user = await create_user(
            db=_db,
            username=req.username,
            email=req.email,
            password=req.password,
            first_name=req.first_name,
            last_name=req.last_name,
        )
    
        if not new_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail= AuthMessages.USER_CREATION_FAILED.value
            )
    
        access_token = _generate_access_token(data={"user_id": str(new_user.id)})
        refresh_token = _generate_refresh_token()
    
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await create_refresh_token(_db, new_user, refresh_token, expires_at)
    
        return APIResponse(
            success= True,
            message= AuthMessages.USER_REGISTERED.value,
            data= AuthResponse(
                access_token= access_token,
                refresh_token= refresh_token
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= AuthMessages.REGISTER_ERROR.value
        ) from e

async def login(req: LoginRequest, _db: AsyncSession) -> APIResponse[AuthResponse]:
    try:
        user = await verify_users_pwd(db=_db, email=req.email, pwd=req.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= AuthMessages.WRONG_INFORMATION.value
            )

        access_token = _generate_access_token(data={"user_id": str(user.id)})
        refresh_token = _generate_refresh_token()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await create_refresh_token(_db, user, refresh_token, expires_at)

        return APIResponse(
            success= True,
            message= AuthMessages.USER_LOGINED.value,
            data= AuthResponse(
                access_token=access_token,
                refresh_token=refresh_token
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= AuthMessages.LOGIN_ERROR.value
        ) from e

async def me(user_id: str, _db: AsyncSession) -> APIResponse[UserResponse]:
    try:
        user = await get_user_by_id(db=_db, user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= AuthMessages.USER_NOT_FOUND.value
            )

        return APIResponse(
            success= True,
            message= AuthMessages.SUCCESSFULLY_GET_CURRENT_USER.value,
            data= UserResponse(
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                roles=user.roles
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= AuthMessages.ME_ERROR.value
        ) from e

async def logout(req: TokenRequest, _db: AsyncSession) -> APIResponse[bool]:
    try:
        db_token = await get_refresh_token(db=_db, token=req.refresh_token)
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= AuthMessages.TOKEN_NOT_FOUND.value
            )

        await revoke_refresh_token(_db, req.refresh_token)
        await delete_expired_tokens(_db)

        return APIResponse(
            success= True,
            message= AuthMessages.SUCCESSFULLY_LOGOUT.value,
            data = True
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= AuthMessages.LOGOUT_ERROR.value
        ) from e
    
async def refresh(req: TokenRequest, _db: AsyncSession) -> APIResponse[RefreshResponse]:
    try:
        db_token = await get_refresh_token(db=_db, token=req.refresh_token)
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= AuthMessages.TOKEN_NOT_FOUND.value
            )

        access_token = _generate_access_token(data={"user_id": str(db_token.id)})

        return APIResponse(
            success= True,
            message= AuthMessages.TOKEN_REFRESHED.value,
            data= RefreshResponse(
                access_token= access_token
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= AuthMessages.REFRESH_ERROR.value
        ) from e