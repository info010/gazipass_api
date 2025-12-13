from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from core.security.auth import get_current_user
from validators.auth_models import JwtPayload
from validators.post_models import PostRequest
from controllers.post_controller import post_controller as ctrl

from database.database import get_db

router = APIRouter(prefix="/Post", tags=["Post"])

@router.get("")
async def get_all_posts(
    size: int = Query(default=50, le=100),
    offset: int = Query(default=0),
    tags: List[str] =  Query(default=[]),
    search: str = Query(default="", max_length=255),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).get_all_posts(size, offset, tags, search)

@router.get("/{post_id}")
async def get_post(
    post_id: str,
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).get_post(post_id)

@router.post("")
async def create_post(
    req: PostRequest,
    _claims: JwtPayload = Depends(get_current_user),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).create_post(req, _claims)

@router.patch("/{post_id}")
async def update_post(
    post_id: str,
    req: PostRequest,
    _claims: JwtPayload = Depends(get_current_user),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).update_post(post_id ,req, _claims)

@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    _claims: JwtPayload = Depends(get_current_user),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).delete_post(post_id, _claims)

@router.patch("/{post_id}/upvote")
async def upvote_post(
    post_id: str,
    _claims: JwtPayload = Depends(get_current_user),
    _db: AsyncSession = Depends(get_db)
):
    return await ctrl.with_service(_db).upvote_post(post_id, _claims.username)

