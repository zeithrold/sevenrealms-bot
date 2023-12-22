from apscheduler.triggers.cron import CronTrigger
from nonebot import require
from pytz import timezone
from nonebot_plugin_apscheduler import scheduler
import os
from .database import generate_dataset
from .alioss import bucket
from nonebot import require, get_bot, get_driver
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger

require("nonebot_plugin_apscheduler")

driver = get_driver()
driver_config = driver.config


@scheduler.scheduled_job(CronTrigger(hour=0, timezone=timezone("Asia/Shanghai")))
async def _():
    require("sevenrealms_bot.plugins.global_config")

    from sevenrealms_bot.plugins.global_config import global_config

    bot: Bot = get_bot(global_config.qq_self_id)
    superuser = list(driver_config.superusers)[0]
    group_id = int(global_config.qq_main_group)
    try:
        await bot.send_group_msg(group_id=group_id, message=f"[备份] 正在备份聊天信息...")
        full_path, file_name = generate_dataset()
        alioss_file_path = f"message_data/{file_name}"
        bucket.put_object_from_file(alioss_file_path, full_path)
        bucket.put_symlink(alioss_file_path, "message_data/latest.7z")
        os.remove(full_path)
        at = MessageSegment.at(superuser)
        message = MessageSegment.text(f"[备份]文件备份成功，文件名为：{file_name}")
        await bot.send_group_msg(group_id=group_id, message=(at + message))
    except Exception as e:
        logger.warning("文件备份出现了问题，错误信息如下：")
        logger.warning(e)
        at = MessageSegment.at(superuser)
        message = MessageSegment.text(f"[备份]文件备份失败，请查看控制台。")
        await bot.send_group_msg(group_id=group_id, message=(at + message))
        return
