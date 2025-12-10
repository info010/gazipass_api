from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_db
from controllers.user_controller import user_controller as ctrl
from validators.user_models import (
    UpdateUserRequest
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
async def get_all_users(
    size: int = Query(default=50, le=100),
    offset: int = Query(default=0),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).get_all_users(size, offset)


@router.get("/{username}")
async def get_user(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).get_user(username)

@router.patch("/{username}")
async def update_user(username: str, payload: UpdateUserRequest, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).update_user(username)

@router.delete("/{username}")
async def delete_user(username: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).delete_user(username)

@router.post("/{username}/follow-user/{target}")
async def follow_user(username: str, target: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).follow_user(username, target)

@router.delete("/{username}/unfollow-user/{target}")
async def unfollow_user(username: str, target: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).unfollow_user(username, target)

@router.post("/{username}/follow-tag/{target}")
async def follow_tag(username: str, target: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).follow_tag(username, target)

@router.delete("/{username}/unfollow-tag/{target}")
async def unfollow_tag(username: str, target: str, _db: AsyncSession = Depends(get_db)):
    return await ctrl.with_service(_db).unfollow_user(username, target)