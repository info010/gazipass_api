import base64
import os
from datetime import datetime, timedelta, timezone
import uuid

from core.enums.messages import AuthMessages
from validators.auth_models import (
    JwtPayload,
    RegisterRequest,
    LoginRequest,
    TokenRequest,
    AuthResponse,
    AuthUserResponse,
    RefreshResponse
)
from core.common.api_models import APIResponse
from core.security.crypto import create_jwt, verify_pwd, hash_pwd

from core.common.base_service import BaseService
from repositories.user_repository import UserRepository
from repositories.refresh_token_repository import RefreshTokenRepository


class AuthService(BaseService):
    user_repo = UserRepository
    token_repo = RefreshTokenRepository

    def _generate_refresh_token(self) -> str:
        return base64.b64encode(os.urandom(32)).decode("utf-8")

    def _generate_access_token(self, data: JwtPayload, timedelta: timedelta | None = None ) -> str:
        if timedelta:
            data.exp = data.exp + timedelta 
        return create_jwt(data=data)

    async def register(self, req: RegisterRequest) -> APIResponse[AuthResponse]:
        user_repo = self.user_repo(self.db)
        token_repo = self.token_repo(self.db)

        if await user_repo.get_by(email = req.email) or await user_repo.get_by(username = req.username):
            self.error(AuthMessages.EMAIL_EXISTS)

        new_user = await user_repo.create(
            username=req.username,
            email=req.email,
            hashed_password=hash_pwd(req.password),
            first_name=req.first_name,
            last_name=req.last_name
        )

        refresh_token = self._generate_refresh_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        await token_repo.create_token(
            user=new_user,
            token=refresh_token,
            expires_at=expires_at
        )

        access_uuid = uuid.uuid4()

        access_token = self._generate_access_token(
            JwtPayload(
                user_id=new_user.id,
                username=new_user.username,
                roles=new_user.roles,
                iat=datetime.now(timezone.utc),
                exp=datetime.now(timezone.utc) + timedelta(hours=1),
                jti= access_uuid
            )
        )

        return self.success(
            AuthMessages.USER_REGISTERED,
            AuthResponse(access_token=access_token, refresh_token=refresh_token)
        )

    async def login(self, req: LoginRequest) -> APIResponse[AuthResponse]:
        user_repo = self.user_repo(self.db)
        token_repo = self.token_repo(self.db)

        user = await user_repo.get_by(email = req.email)
        if not user:
            self.error(AuthMessages.USER_NOT_FOUND)

        if not verify_pwd(req.password, user.hashed_password):
            self.error(AuthMessages.WRONG_INFORMATION)

        access_uuid = uuid.uuid4()

        access_token = self._generate_access_token(
            JwtPayload(
                user_id=user.id,
                username=user.username,
                roles=user.roles,
                iat=datetime.now(timezone.utc),
                exp=datetime.now(timezone.utc) + timedelta(hours=1),
                jti=access_uuid
            )
        )
        refresh_token = self._generate_refresh_token()

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        await token_repo.create_token(
            user=user,
            token=refresh_token,
            expires_at=expires_at
        )

        return self.success(
            AuthMessages.USER_LOGINED,
            AuthResponse(access_token=access_token, refresh_token=refresh_token)
        )

    async def me(self, user_id: str) -> APIResponse[AuthUserResponse]:
        user_repo = self.user_repo(self.db)

        user = await user_repo.get(user_id)
        if not user:
            self.error(AuthMessages.USER_NOT_FOUND, 404)

        return self.success(
            AuthMessages.SUCCESSFULLY_GET_CURRENT_USER,
            AuthUserResponse(
                username=user.username,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                roles=user.roles
            )
        )

    async def logout(self, user_id: str) -> APIResponse[bool]:
        token_repo = self.token_repo(self.db)

        token = await token_repo.get_active_by_user(user_id)
        if not token:
            self.error(AuthMessages.TOKEN_NOT_FOUND, 404)

        await token_repo.revoke(token.token)

        return self.success(AuthMessages.SUCCESSFULLY_LOGOUT, True)

    async def refresh(self, user_id: str, req: TokenRequest) -> APIResponse[RefreshResponse]:
        user_repo = self.user_repo(self.db)
        token_repo = self.token_repo(self.db)

        db_token = await token_repo.get_by(
            user_id = user_id,
            token = req.refresh_token
        )

        if not db_token:
            self.error(AuthMessages.TOKEN_NOT_FOUND, 404)

        user = await user_repo.get(db_token.user_id)

        access_uuid = uuid.uuid4()

        new_access_token = self._generate_access_token(
            JwtPayload(
                user_id=user.id,
                username=user.username,
                roles=user.roles,
                iat=datetime.now(timezone.utc),
                exp=datetime.now(timezone.utc) + timedelta(hours=1),
                jti=access_uuid
            )
        )

        return self.success(
            AuthMessages.TOKEN_REFRESHED,
            RefreshResponse(access_token=new_access_token)
        )