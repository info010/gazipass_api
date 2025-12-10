from fastapi import APIRouter
from api.v1.routers import auth, user

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(router=auth.router)
v1_router.include_router(router=user.router)