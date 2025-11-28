from fastapi import APIRouter, FastAPI
from api.v1.router import v1_router

routers = APIRouter(prefix="/api")

versioned_routers = [v1_router]

@routers.get(
    "/health",
    tags=["System"]
)
async def health():
    return {
        "success": True,
        "message": "Server health is fetched",
        "data": {"health": "Server health is now good."}
    }

def setup_routers(app: FastAPI):
    for r in versioned_routers:
        routers.include_router(router=r)
    app.include_router(router=routers)
