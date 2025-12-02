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