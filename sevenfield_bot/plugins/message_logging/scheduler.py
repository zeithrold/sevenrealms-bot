import asyncio
from nonebot import require, get_bot
from nonebot.adapters.onebot.v11 import Bot
from .count import get_count
from .config import config

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
from apscheduler.triggers.cron import CronTrigger

@scheduler.scheduled_job("cron", second=5)
async def _():
    require("sevenfield_bot.plugins.global_config")
    from sevenfield_bot.plugins.global_config import global_config
    bot: Bot = get_bot(global_config.qq_self_id)
    counts = get_count()
    groups = config.qq_logging_group
    message = ("当前时间为：00:00。\n"
                f"目前，小小Z已经收集了共{counts}条消息。"
                "\n"
                "若不愿意被收集聊天记录，请输入命令 /blacklist 以查询黑名单功能。\n"
                "是时候该睡觉了，小小Z祝各位有个好梦，晚安🌟"
    )
    await bot.send_group_msg(group_id=int(global_config.qq_main_group), message=message)
    # task_list = []
    # for group in groups:
    #     task_list.append(bot.send_group_msg(group_id=int(group), message=message))
    # await asyncio.gather(task_list)
