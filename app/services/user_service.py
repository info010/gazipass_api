from typing import List
from repositories.tag_repository import TagRepository
from repositories.post_repository import PostRepository
from core.common.base_service import BaseService
from core.enums.messages import UserMessages
from repositories.user_repository import UserRepository
from validators.user_models import UpdateUserRequest, UserResponse
from core.common.api_models import APIResponse


class UserService(BaseService):
    user_repo = UserRepository
    post_repo = PostRepository
    tag_repo = TagRepository

    async def _build_user_response_single(self, user):
        return UserResponse(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            roles=user.roles,
            created_at=user.created_at.isoformat()
        )
    
    async def _build_user_response(self, data):
        if not isinstance(data, (list, tuple, set)):
            return await self._build_user_response_single(data)
        results = []
        for u in data:
            results.append(await self._build_user_response_single(u))
        return results


    async def get_all_users(self, size: int, offset: int) -> APIResponse[List[UserResponse]]:
        user_repo = self.user_repo(self.db)
        rows = await user_repo.list(size=size, offset=offset)
        users = await self._build_user_response([r for r in rows])
        return self.success(UserMessages.GET_ALL_USERS, users)

    async def get_user(self, username: str) -> APIResponse[UserResponse]:
        repo = self.user_repo(self.db)
        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)
        return self.success(
            UserMessages.GET_USER, 
            await self._build_user_response(user)
        )

    async def update_user(self, username: str, payload: UpdateUserRequest) -> APIResponse[UserResponse]:
        repo = self.user_repo(self.db)
        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)
        updated = await repo.update(user, payload.dict(exclude_unset=True))
        return self.success(
            UserMessages.USER_UPDATED,
            await self._build_user_response(updated)
        )
    
    async def get_followers(self, username: str):
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        try:
            return await repo.fetch_followers_ids(user.id)
        except Exception as e:
            self.error(str(e), 500)

    async def get_followed_users(self, username: str):
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        try:
            return await repo.fetch_followed_users_ids(user.id)
        except Exception as e:
            self.error(str(e), 500)

    async def follow_user(self, username: str, current_user: str, target: str) -> APIResponse[bool]:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_user = await repo.get_by(username=target)
        if not target_user:
            self.error(UserMessages.USER_NOT_FOUND, 404)
        
        user_followerd_users = await repo.fetch_followed_users_ids(user.id)
        if target_user.id in user_followerd_users:
            self.error(UserMessages.ALREADY_FOLLOWING, 409)

        try:
            await repo.append_followers(user.id, target_user.id)
            await self.db.commit()
        except Exception as e:
            self.error(str(e), 500)

        return self.success(UserMessages.USER_FOLLOWED, True)

    async def unfollow_user(self, username: str, current_user: str, target: str) -> APIResponse[bool]:
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_user = await repo.get_by(username=target)
        if not target_user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        user_followerd_users = await repo.fetch_followed_users_ids(user.id)
        if target_user.id not in user_followerd_users:
            self.error(UserMessages.NOT_FOLLOWING, 409)

        try:
            await repo.pop_followers(user.id, target_user.id)
            await self.db.commit()
        except Exception as e:
            self.error(str(e), 500)

        return self.success(UserMessages.USER_UNFOLLOWED, True)
    
    async def get_followed_tags(self, username: str):
        repo = self.user_repo(self.db)

        user = await repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        try:
            return await repo.fetch_followed_tags_ids(user.id)
        except Exception as e:
            self.error(str(e), 500)

    async def follow_tag(self, username: str, current_user: str, tag: str) -> APIResponse[bool]:
        user_repo = self.user_repo(self.db)
        tag_repo = self.tag_repo(self.db)

        user = await user_repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_tag = await tag_repo.get_by(tag=tag)
        user_followed_tags = await user_repo.fetch_followed_tags_ids(user.id)
        if target_tag.id in user_followed_tags:
            self.error(UserMessages.ALREADY_FOLLOWING, 409)

        try:
            await user_repo.append_followed_tags(user.id, target_tag.id)
            await self.db.commit()
        except Exception as e:
            self.error(str(e), 500)

        return self.success(UserMessages.TAG_FOLLOWED, True)

    async def unfollow_tag(self, username: str, current_user: str, tag: str) -> APIResponse[bool]:
        user_repo = self.user_repo(self.db)
        tag_repo = self.tag_repo(self.db)

        user = await user_repo.get_by(username=username)
        if not user:
            self.error(UserMessages.USER_NOT_FOUND, 404)

        target_tag = await tag_repo.get_by(tag=tag)
        user_followed_tags = await user_repo.fetch_followed_tags_ids(user.id)
        if target_tag.id not in user_followed_tags:
            self.error(UserMessages.NOT_FOLLOWING, 409)

        try:
            await user_repo.pop_followed_tags(user.id, target_tag.id)
            await self.db.commit()
        except Exception as e:
            self.error(str(e), 500)

        return self.success(UserMessages.TAG_UNFOLLOWED, True)
