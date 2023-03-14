from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    about_template: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
