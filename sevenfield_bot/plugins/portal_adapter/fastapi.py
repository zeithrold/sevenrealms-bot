from nonebot import require
from fastapi import FastAPI
from .middleware import AccessTokenMiddleware
from .user import user_app

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# app.add_middleware(AccessTokenMiddleware)

app.mount("/user", user_app)

@app.get("/")
async def handler():
    return {"status": "ok"}

