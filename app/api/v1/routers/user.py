from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer

from api.v1.validators.user_models import UserResponse
from api.v1.validators.common.api_models import APIResponse
from core.security.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
router = APIRouter(prefix="/User", tags=["User"])

@router.get(
    "/",
    summary= "Get all users",
    response_model=APIResponse[List[UserResponse]]
)
async def get_all_users(query: str = Query(max_length=50), page: int = 0, size: int = 20):
    return await user_controller.get_all_users(query, page, size)

@router.get(
    "/me",
    summary="Get current User",
    response_model=APIResponse[UserResponse]
)
async def me(_claims: dict = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await user_controller.me(_claims["user_id"], _db)

@router.get(
    "/{username}",
    summary="Get the User has this username",
    response_model=APIResponse[UserResponse]
)
async def get_user(username: str, _db: AsyncSession = Depends(get_db)):
    return await user_controller.get_user(username, _db)

@router.get(
    "/{username}/posts",
    summary="Get the user's posts",
    response_model=APIResponse[List[UUID]]
)
async def get_user_posts(username: str, page: int = 0, size: int = 20, _db: AsyncSession = Depends(get_db)):
    return await user_controller.get_user_posts(username, page, size, _db)

@router.get(
    "/{username}/upvoted_posts",
    summary="Get the user's upvoted posts",
    response_model=APIResponse[List[UUID]]
)
async def get_user_posts(username: str, page: int = 0, size: int = 20, _db: AsyncSession = Depends(get_db)):
    return await user_controller.get_user_posts(username, page, size, _db)