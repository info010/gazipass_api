from core.common.base_repository import BaseRepository
from database.models.post import Post


class PostRepository(BaseRepository[Post]):
    model = Post