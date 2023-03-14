from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    alinlp_accesskey_id: str
    alinlp_accesskey_secret: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
