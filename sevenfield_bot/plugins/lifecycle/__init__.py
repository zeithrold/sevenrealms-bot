from nonebot import require, get_driver
import time

driver = get_driver()

@driver.on_startup
def handler():
    require("sevenfield_bot.plugins.db")
    from sevenfield_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="startup")
        orm.commit()

@driver.on_shutdown
def handler():
    require("sevenfield_bot.plugins.db")
    from sevenfield_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="shutdown")
        orm.commit()

@driver.on_bot_connect
def handler():
    require("sevenfield_bot.plugins.db")
    from sevenfield_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="bot_connect")
        orm.commit()

@driver.on_bot_disconnect
def handler():
    require("sevenfield_bot.plugins.db")
    from sevenfield_bot.plugins.db import Lifecycle
    from pony import orm
    with orm.db_session:
        Lifecycle(time=int(time.time()), type="bot_disconnect")
        orm.commit()
