from sqlalchemy import delete, select, insert
from database.models.user import User
from core.common.base_repository import BaseRepository
from database.models.user import user_followed_tags, user_followed_users


class UserRepository(BaseRepository[User]):
    model = User

    async def fetch_followers_ids(self, id):
        stmt = (
            select(user_followed_users.c.user_id)
            .where(user_followed_users.c.creator_id == id)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def fetch_followed_users_ids(self, id):
        stmt = (
            select(user_followed_users.c.creator_id)
            .where(user_followed_users.c.user_id == id)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()

    async def fetch_followed_tags_ids(self, id):
        stmt = (
            select(user_followed_tags.c.tag_id)
            .where(user_followed_tags.c.user_id == id)
        )
        res = await self.db.execute(stmt)
        return res.scalars().all()
    
    async def append_followers(self, id, target_id):
        stmt = (
            insert(user_followed_users)
            .values(
                user_id = id,
                creator_id = target_id
            )
        )
        await self.db.execute(stmt)
    
    async def pop_followers(self, id, target_id):
        stmt = (
            delete(user_followed_users)
            .where(
                user_followed_users.c.user_id == id,
                user_followed_users.c.creator_id == target_id
            )
        )
        await self.db.execute(stmt)
    
    async def append_followed_tags(self, id, target_id):
        stmt = (
            insert(user_followed_users)
            .values(
                user_id = id,
                tag_id = target_id
            )
        )
        await self.db.execute(stmt)
    
    async def pop_followed_tags(self, id, target_id):
        stmt = (
            delete(user_followed_users)
            .where(
                user_followed_users.c.user_id == id,
                user_followed_users.c.tag_id == target_id
            )
        )
        await self.db.execute(stmt)