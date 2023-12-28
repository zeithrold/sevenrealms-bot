from redis import Redis
from nonebot.log import logger
from .config import config

client = Redis(
    host=config.redis_host,
    port=config.redis_port,
    db=config.redis_db,
    decode_responses=True
)

logger.info("Redis connected.")
client.ping()
logger.info("Redis pinged.")
