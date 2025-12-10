from sqlalchemy import select
from database.models.user import User
from core.security.crypto import hash_pwd
from core.common.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_email(self, email: str):
        q = select(User).where(User.email == email)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def get_by_username(self, username: str):
        q = select(User).where(User.username == username)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def create_user(self, **data):
        data["hashed_password"] = hash_pwd(data.pop("password"))
        return await self.create(data)
