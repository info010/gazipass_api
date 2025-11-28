from datetime import datetime, timezone
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.refresh_token import RefreshToken
from database.models.user import User


async def create_refresh_token(db: AsyncSession, user: User, token: str, expires_at: datetime) -> RefreshToken:
    """Yeni bir refresh token oluşturur."""
    db_token = RefreshToken(
        token=token,
        expires_at=expires_at,
    )
    db_token.user = user
    exists = await get_refresh_token_by_user(db=db, user_id=user.id)
    if exists:
        await revoke_refresh_token(db=db , token=exists.token)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def get_refresh_token(db: AsyncSession, token: str) -> RefreshToken | None:
    """Token string'ine göre refresh token kaydını döndürür."""
    q = select(RefreshToken).where(RefreshToken.token == token)
    res = await db.execute(q)
    token = res.scalar_one_or_none()
    if not token or token.revoked_at:
        return None
    return token

async def get_refresh_token_by_user(db: AsyncSession, user_id) -> RefreshToken | None:
    q = (
        select(RefreshToken)
        .where(RefreshToken.user_id == user_id, RefreshToken.revoked_at.is_(None))
        .order_by(RefreshToken.created_at.desc())
        .limit(1)
    )
    res = await db.execute(q)
    return res.scalar_one_or_none()


async def revoke_refresh_token(db: AsyncSession, token: str) -> bool:
    """Refresh token'ı geçersiz hale getirir (revoked_at alanını doldurur)."""
    q = (
        update(RefreshToken)
        .where(RefreshToken.token == token)
        .values(revoked_at=datetime.now(timezone.utc))
    )
    await db.execute(q)
    await db.commit()
    return True


async def delete_expired_tokens(db: AsyncSession) -> int:
    """Süresi dolmuş refresh token'ları temizler."""
    q = delete(RefreshToken).where(RefreshToken.expires_at < datetime.now(timezone.utc))
    result = await db.execute(q)
    await db.commit()
    return result.rowcount
