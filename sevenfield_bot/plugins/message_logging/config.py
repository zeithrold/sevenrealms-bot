from nonebot import get_driver
from pydantic import BaseModel, Extra
from typing import List


class Config(BaseModel, extra=Extra.ignore):
    qq_logging_group: List[str] = []


_driver = get_driver()
config = Config.parse_obj(_driver.config)
