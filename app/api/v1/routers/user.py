from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from validators.auth_models import JwtPayload
from core.enums.permission import UserRole
from core.security.auth import get_current_user, required_roles
from database.database import get_db
from controllers.user_controller import user_controller as ctrl
from validators.user_models import (
    UpdateUserRequest
)

router = APIRouter(prefix="/Users", tags=["Users"])

@router.get("")
async def get_all_users(
    size: int = Query(default=50, le=100),
    offset: int = Query(default=0),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).get_all_users(size, offset)

@router.get("/me")
async def get_me(_claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_user(_claims.username)

@router.patch("/me")
async def get_me(payload: UpdateUserRequest, _claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).update_user(_claims.username, payload)

@router.get("/{username}")
async def get_user(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_user(username)

@router.patch(
        "/{username}",
        dependencies=[required_roles(UserRole.ADMIN)]   
    )
async def update_user(username: str, payload: UpdateUserRequest, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).update_user(username, payload)

@router.get("/followers/{username}")
async def get_followed_users(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_followers(username)

@router.get("/followed-users/{username}")
async def get_followed_users(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_followed_users(username)

@router.patch("/followed-users/{target}")
async def follow_user(target: str, _claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).follow_user(_claims.username, target)

@router.delete("/followed-users/{target}")
async def unfollow_user(target: str, _claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).unfollow_user(_claims.username, target)

@router.get("/followed-tags/{username}")
async def get_followed_users(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_followed_tags(username)

@router.patch("/followed-tags/{target}")
async def follow_tag(target: str, _claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).follow_tag(_claims.username, target)

@router.delete("/followed-tags/{target}")
async def unfollow_tag(target: str, _claims: JwtPayload = Depends(get_current_user), _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).unfollow_user(_claims.username, target)