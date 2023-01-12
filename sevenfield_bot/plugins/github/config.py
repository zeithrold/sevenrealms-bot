from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    github_access_token: str
    github_api_endpoint: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
