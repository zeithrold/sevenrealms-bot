from nonebot import require
from fastapi import FastAPI
from .middleware import AccessTokenMiddleware

app = FastAPI()

app.add_middleware(AccessTokenMiddleware)


@app.get("/")
async def handler():
    return {"status": "ok"}


@app.get("/counts")
async def counts_handler():
    require("sevenfield_bot.plguins.message_logging")
    from sevenfield_bot.plugins.message_logging.count import get_count
    count = get_count()
    return {
        "counts": count
    }
