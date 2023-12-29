from redis.asyncio.client import Redis
from nonebot import get_driver
from nonebot.log import logger
from .config import config

client = Redis(
    host=config.redis_host,
    port=config.redis_port,
    db=config.redis_db,
    decode_responses=True
)

driver = get_driver()

@driver.on_startup
async def _():
    logger.info("Redis connected.")
    await client.ping()
    logger.info("Redis pinged.")
