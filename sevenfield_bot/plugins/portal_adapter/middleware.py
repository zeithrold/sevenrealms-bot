from fastapi import status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .config import config


class AccessTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        access_token = request.headers.get("Authorization", "").strip()
        if "Bearer " + config.portal_access_token != access_token and not (request.url.path.endswith("/docs") or request.url.path.endswith("/openapi.json")):
            return JSONResponse({
                "error": "invalid_access_token"
            }, status_code=401)
        response = await call_next(request)
        return response
