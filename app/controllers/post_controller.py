from core.common.base_controller import BaseController
from services.post_service import PostService

class PostController(BaseController[PostService]):
    def __init__(self):
        super().__init__(PostService)

post_controller = PostController()