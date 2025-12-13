from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from validators.auth_models import JwtPayload
from core.security.crypto import verify_jwt
from core.enums.permission import UserRole

bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> JwtPayload:
    return verify_jwt(credentials.credentials)
    
def required_roles(*required: UserRole):
    async def wrapper(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
    ):
        payload = verify_jwt(credentials.credentials)
        user_roles = set(payload.roles)
        required_roles = set(r.name for r in required)
    
        if not (user_roles & required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission for this operation."
            )
    return Depends(wrapper)