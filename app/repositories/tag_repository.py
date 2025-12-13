from database.models.tag import Tag
from core.common.base_repository import BaseRepository


class TagRepository(BaseRepository[Tag]):
    model = Tag