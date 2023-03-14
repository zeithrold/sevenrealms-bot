from nonebot import get_driver
from pydantic import BaseModel, Extra
from typing import Set


class Config(BaseModel, extra=Extra.ignore):
    alioss_accesskey_id: str
    alioss_accesskey_secret: str
    alioss_endpoint: str
    alioss_bucket: str
    alioss_encrypt_password: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
