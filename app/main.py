import asyncio

from fastapi import APIRouter, FastAPI, HTTPException, Request, logger
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from middleware.response_wrapper import ResponseWrapperMiddleware
from database.init_db import init_db
from utils.logger import setup_logging, logger
from api.api_router import setup_routers, versioned_routers

app = FastAPI(
    title="GaziPass API",
    version="0.0.1",
    description="",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(ResponseWrapperMiddleware)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error on %s %s: %s", request.method, request.url, exc.errors())
    return JSONResponse(
        status_code=422,
        content={"success": False, "message": "Validation error", "errors": exc.errors()},
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal Server Error"},
    )

setup_routers(app)

if __name__ == "__main__":
    setup_logging()
    import asyncio
    asyncio.run(init_db())
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=10000,
        reload=True
    )