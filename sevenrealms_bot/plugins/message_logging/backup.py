import os

from apscheduler.triggers.cron import CronTrigger
from nonebot import get_bot, get_driver, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_datastore import create_session
from pytz import timezone
from sevenrealms_bot.plugins.global_config import global_config

matcher = on_command("backup", permission=SUPERUSER)

from .alioss import bucket
from .file import generate_dataset

driver = get_driver()
driver_config = driver.config


job = scheduler.scheduled_job(CronTrigger(hour=0, timezone=timezone("Asia/Shanghai")))


async def backup_handler():
    bot: Bot = get_bot(global_config.qq_self_id)  # type: ignore
    superuser = list(driver_config.superusers)[0]
    group_id = int(global_config.qq_main_group)
    try:
        await bot.send_group_msg(group_id=group_id, message=f"[备份] 正在备份聊天信息...")
        async with create_session() as session:
            full_path, file_name = await generate_dataset(session)
        alioss_file_path = f"message_data/{file_name}"
        logger.info('Uploading to Aliyun OSS...')
        bucket.put_object_from_file(alioss_file_path, full_path)
        bucket.put_symlink(alioss_file_path, "message_data/latest.7z")
        logger.success('Successfully upload file to Aliyun OSS.')
        os.remove(full_path)
        at = MessageSegment.at(superuser)
        message = MessageSegment.text(f" [备份]文件备份成功，文件名为：{file_name}")
        await bot.send_group_msg(group_id=group_id, message=(at + message))
    except Exception as e:
        logger.warning("文件备份出现了问题，错误信息如下：")
        logger.warning(e)
        at = MessageSegment.at(superuser)
        message = MessageSegment.text(f" [备份]文件备份失败，请查看控制台。")
        await bot.send_group_msg(group_id=group_id, message=(at + message))
        return


job(backup_handler)
matcher.handle()(backup_handler)
