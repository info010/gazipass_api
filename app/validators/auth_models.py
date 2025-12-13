from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

from core.enums.permission import UserRole

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthUserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    roles: list[str]

class TokenRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str

class JwtPayload(BaseModel):
    user_id: UUID
    username: str
    roles: list[str] = Field(default_factory=lambda: [UserRole.DEFAULT.name])
    iat: datetime
    exp: datetime
    jti: UUID