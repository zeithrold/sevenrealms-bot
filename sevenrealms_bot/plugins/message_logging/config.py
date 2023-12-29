from typing import Set

from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    qq_logging_group: Set[str] = set()
    alioss_accesskey_id: str
    alioss_accesskey_secret: str
    alioss_endpoint: str
    alioss_bucket: str
    alioss_encrypt_password: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
