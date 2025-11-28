import datetime
from bcrypt import hashpw, gensalt, checkpw
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status

from .config import JWT_ALGORITHM, JWT_SECRET_KEY

bearer_scheme = HTTPBearer()

def hash_pwd(pwd: str) -> str:
    return hashpw(pwd.encode(), gensalt()).decode()

def verify_pwd(pwd: str, hash: str) -> bool:
    return checkpw(pwd.encode(), hash.encode())

def create_jwt(data: dict, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0) -> str:
    to_encode = data.copy()
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )