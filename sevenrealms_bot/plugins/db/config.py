from nonebot import get_driver
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    mysql_host = '127.0.0.1'
    mysql_port = 3306
    mysql_user: str
    mysql_password: str
    mysql_database: str


_driver = get_driver()
config = Config.parse_obj(_driver.config)
