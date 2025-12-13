from repositories.post_repository import PostRepository
from core.common.base_service import BaseService


class PostService(BaseService):
    post_repo = PostRepository