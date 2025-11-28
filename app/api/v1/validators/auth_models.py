from pydantic import BaseModel, EmailStr

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

class UserResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    roles: list[str]

class TokenRequest(BaseModel):
    refresh_token: str

class LogoutResponse(BaseModel):
    success: bool
    message: str

class RefreshResponse(BaseModel):
    success: bool
    message: str
    access_token: str