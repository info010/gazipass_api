from database.models.comment import Comment
from core.common.base_repository import BaseRepository


class CommentRepository(BaseRepository[Comment]):
    model = Comment