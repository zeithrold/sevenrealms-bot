from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    redis_host = "localhost"
    redis_port = 6379
    redis_db = 0

_driver = get_driver()
config = Config.parse_obj(_driver.config)
