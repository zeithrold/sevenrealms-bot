from nonebot import get_driver
from pydantic import BaseModel, Extra
from typing import Set


class Config(BaseModel, extra=Extra.ignore):
    qq_blacklist_group: Set[str] = set()
    qq_self_id: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
