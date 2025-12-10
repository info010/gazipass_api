from fastapi import APIRouter

class BaseRouter(APIRouter):
    def __init__(self, prefix: str, tags: list):
        super().__init__(prefix=prefix, tags=tags)