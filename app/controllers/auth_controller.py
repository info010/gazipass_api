from core.common.base_controller import BaseController
from services.auth_service import AuthService

class AuthController(BaseController[AuthService]):
    def __init__(self):
        super().__init__(AuthService)

auth_controller = AuthController()