from .fastapi import app as sub_app
from nonebot import get_driver
from nonebot.drivers.fastapi import Driver

driver: Driver = get_driver()
app = driver.server_app


app.mount("/portal", sub_app)
