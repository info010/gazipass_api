from core.common.base_controller import BaseController
from services.user_service import UserService

class UserController(BaseController[UserService]):
    def __init__(self):
        super().__init__(UserService)

user_controller = UserController()