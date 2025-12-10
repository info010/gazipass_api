from database.models.user import User
from core.common.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User