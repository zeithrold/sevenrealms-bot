from nonebot import get_driver
from .config import Config


driver = get_driver()
global_config = Config.parse_obj(driver.config)
