import datetime
from uuid import UUID
from bcrypt import hashpw, gensalt, checkpw
from jose import jwt, JWTError
from fastapi import HTTPException, status

from validators.auth_models import JwtPayload
from utils.config import JWT_ALGORITHM, JWT_SECRET_KEY

def hash_pwd(pwd: str) -> str:
    return hashpw(pwd.encode(), gensalt()).decode()

def verify_pwd(pwd: str, hash: str) -> bool:
    return checkpw(pwd.encode(), hash.encode())

def create_jwt(data: JwtPayload) -> str:
    to_encode = data.model_dump()
    to_encode["user_id"] = str(to_encode["user_id"])
    to_encode["jti"] = str(to_encode["jti"])
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_jwt(token: str) -> JwtPayload:
    try:
        res = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return JwtPayload(
            user_id=UUID(res["user_id"]),
            username=res["username"],
            roles=res["roles"],
            iat=res["iat"],
            exp=res["exp"],
            jti=UUID(res["jti"])
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )