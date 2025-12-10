from datetime import datetime, timezone
from sqlalchemy import select, update, delete

from database.models.refresh_token import RefreshToken
from database.models.user import User
from core.common.base_repository import BaseRepository

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    model = RefreshToken

    async def get_by_token(self, token: str):
        return await self.get_by(token=token)

    async def get_active_by_user(self, user_id: str) -> RefreshToken | None:
        """Kullanıcının aktif olan (revoked olmayan) son refresh token'ı"""
        q = (
            select(self.model)
            .where(self.model.user_id == user_id, self.model.revoked_at.is_(None))
            .order_by(self.model.created_at.desc())
            .limit(1)
        ) 
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def create_token(self, user: User, token: str, expires_at: datetime) -> RefreshToken:
        """Yeni refresh token oluşturur ve varsa eskiyi revoke eder."""
        existing = await self.get_active_by_user(user.id)
        if existing:
            await self.revoke(existing.token)

        new_token = RefreshToken(
            token=token,
            expires_at=expires_at,
            user=user
        )

        return await self.create(new_token)

    async def revoke(self, token: str) -> bool:
        """Token'ı revoke eder."""
        q = (
            update(self.model)
            .where(self.model.token == token)
            .values(revoked_at=datetime.now(timezone.utc))
        )
        await self.db.execute(q)
        await self.db.commit()
        return True

    async def delete_expired(self) -> int:
        """Süresi dolmuş tokenları siler."""
        q = delete(self.model).where(self.model.expires_at < datetime.now(timezone.utc))
        result = await self.db.execute(q)
        await self.db.commit()
        return result.rowcount
