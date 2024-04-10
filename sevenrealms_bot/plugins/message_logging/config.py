from typing import Set

from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    qq_logging_group: Set[str] = set()
    qq_self_id: str
    qq_main_group: str
    hf_token: str
    hf_repo: str
    datastore_database_url: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
