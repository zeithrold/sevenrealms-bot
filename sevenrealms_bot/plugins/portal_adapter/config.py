from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    portal_access_token: str

_driver = get_driver()
config = Config.parse_obj(_driver.config)
