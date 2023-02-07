from apscheduler.triggers.cron import CronTrigger
from nonebot import require
from pytz import timezone
from nonebot_plugin_apscheduler import scheduler
from .database import generate_dataset
from .alioss import bucket
from nonebot import require, get_bot, get_driver
from nonebot.adapters.onebot.v11 import Bot
from nonebot.log import logger

require("nonebot_plugin_apscheduler")

driver = get_driver()
driver_config = driver.config


@scheduler.scheduled_job(CronTrigger(minute="*/10", timezone=timezone("Asia/Shanghai")))
async def _():
    require("sevenfield_bot.plugins.global_config")

    from sevenfield_bot.plugins.global_config import global_config

    bot: Bot = get_bot(global_config.qq_self_id)
    superuser = list(driver_config.superusers)[0]
    group_id = int(global_config.qq_main_group)
    try:
        await bot.send_group_msg(group_id=group_id, message=f"[备份] 正在备份聊天信息...")
        full_path, file_name = generate_dataset()
        alioss_file_path = f'message_data/{file_name}'
        bucket.put_object_from_file(alioss_file_path, full_path)
        bucket.put_symlink(alioss_file_path, "latest.7z")
        await bot.send_group_msg(group_id=group_id, message=f'[CQ:at,qq={superuser}][备份]文件 "{file_name}" 上传成功。')
    except Exception as e:
        logger.warning("文件备份出现了问题，错误信息如下：")
        logger.warning(e)
        await bot.send_group_msg(group_id=group_id, message=f"[CQ:at,qq={superuser}][备份]文件上传失败，请查看控制台。")
        return
