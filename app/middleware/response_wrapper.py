from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json

def make_response(success: bool, message: str, data):
    return {
        "success": success,
        "message": message,
        "data": data
    }

class ResponseWrapperMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/docs") or request.url.path.startswith("/redoc") or request.url.path.startswith("/openapi.json"):
            return await call_next(request)

        response = await call_next(request)

        if response.headers.get("content-type") != "application/json":
            return response

        body = [section async for section in response.body_iterator]
        raw = b"".join(body).decode()

        try:
            content = json.loads(raw)
        except Exception:
            return response

        status = response.status_code
        success = 200 <= status < 300

        message = content.get("message", "")
        data = content.get("data", content)

        wrapped = make_response(success, message, data)

        return JSONResponse(status_code=status, content=wrapped)
