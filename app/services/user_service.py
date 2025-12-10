from typing import List
from core.common.base_service import BaseService
from core.enums.messages import UserMessages
from repositories.user_repository import UserRepository
from validators.user_models import UpdateUserRequest, UserResponse
from core.common.api_models import APIResponse


class UserService(BaseService):
    user_repo = UserRepository

    async def get_all_users(self, size: int, offset: int) -> APIResponse[List[UserResponse]]:
        user_repo = self.user_repo(self.db)
        rows = await user_repo.list(size=size, offset=offset)
        users = [
            UserResponse(
                username=u.username,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                roles=u.roles,
                # posts=[str(p.id) for p in u.posts],
                # upvoted_posts=[str(p.id) for p in u.upvoted_posts],
                # followers=[str(f.id) for f in u.followers],
                # followed_users=[str(fu.id) for fu in u.followed_users],
                # followed_tags=[str(ft.id) for ft in u.followed_tags],
                created_at=str(u.created_at.isoformat())
            ) for u in rows
        ]
        return self.success(UserMessages.GET_ALL_USERS, users)

    async def get_user(self, username: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        return self.success(UserMessages.GET_USER, user)

    async def update_user(self, username: str, payload: UpdateUserRequest) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        updated = await repo.update(user, payload.dict(exclude_unset=True))
        return self.success(UserMessages.USER_UPDATED, updated)

    async def delete_user(self, username: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        await repo.delete(user)
        return self.success(UserMessages.USER_DELETED, True)

    async def follow_user(self, username: str, target: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_user = await repo.get_by(username=target)
        if not target_user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        if target_user.id in user.followers:
            self.error(UserMessages.ALREADY_FOLLOWING, 304)

    # Hata verebilir
        user.followers.append(target_user)
        await self.db.commit()

        return self.success(UserMessages.USER_FOLLOWED, True)

    async def unfollow_user(self, username: str, target: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_user = await repo.get_by(username=target)
        if not target_user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        if target_user.id not in user.followers:
            self.error(UserMessages.NOT_FOLLOWING, 304)

        user.following.remove(target_user)
        await self.db.commit()

        return self.success(UserMessages.USER_UNFOLLOWED, True)

    async def follow_tag(self, username: str, tag: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        if tag in user.followed_tags:
            self.error(UserMessages.ALREADY_FOLLOWING)

        user.followed_tags.append(tag)
        await self.db.commit()

        return self.success(UserMessages.TAG_FOLLOWED, True)

    async def unfollow_tag(self, username: str, tag: str) -> APIResponse:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        if tag not in user.followed_tags:
            self.error(UserMessages.NOT_FOLLOWING)

        user.followed_tags.remove(tag)
        await self.db.commit()

        return self.success(UserMessages.TAG_UNFOLLOWED, True)
