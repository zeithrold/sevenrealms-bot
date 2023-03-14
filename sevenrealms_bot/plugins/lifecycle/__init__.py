from nonebot import require, get_driver
from nonebot.adapters import Bot
from nonebot.adapters.onebot.v11 import Bot as OnebotBot
import time

driver = get_driver()


@driver.on_startup
def handler():
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="startup")
        orm.commit()


@driver.on_shutdown
def handler():
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="shutdown")
        orm.commit()


@driver.on_bot_connect
def handler(bot: Bot):
    require("sevenrealms_bot.plugins.global_config")
    from sevenrealms_bot.plugins.global_config import global_config
    if isinstance(bot, OnebotBot):
        require("sevenrealms_bot.plugins.db")
        from pony import orm
        from sevenrealms_bot.plugins.db import Lifecycle
        with orm.db_session:
            Lifecycle(time=int(time.time()), type="bot_connect")
            orm.commit()
        bot.send_group_msg(group_id=int(global_config.qq_main_group),
                           message=f"[CQ:at,qq={list(driver.config.superusers)[0]}]您的机器人已连接。")


@driver.on_bot_disconnect
def handler(bot: Bot):
    require("sevenrealms_bot.plugins.global_config")
    from sevenrealms_bot.plugins.global_config import global_config
    if isinstance(bot, OnebotBot):
        require("sevenrealms_bot.plugins.db")
        from pony import orm
        from sevenrealms_bot.plugins.db import Lifecycle
        with orm.db_session:
            Lifecycle(time=int(time.time()), type="bot_connect")
            orm.commit()
        bot.send_group_msg(group_id=int(global_config.qq_main_group),
                           message=f"[CQ:at,qq={list(driver.config.superusers)[0]}]您的机器人已断开。")
