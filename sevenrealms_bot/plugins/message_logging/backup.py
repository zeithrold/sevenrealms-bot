from apscheduler.triggers.cron import CronTrigger
from nonebot import get_bot, get_driver, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from datasets import Dataset
from pytz import timezone
import datetime


matcher = on_command("backup", permission=SUPERUSER)

from .config import config

driver = get_driver()
driver_config = driver.config


job = scheduler.scheduled_job(CronTrigger(hour=0, timezone=timezone("Asia/Shanghai")))


async def backup_handler():
    bot: Bot = get_bot(config.qq_self_id)  # type: ignore
    superuser = list(driver_config.superusers)[0]
    group_id = int(config.qq_main_group)
    try:
        await bot.send_group_msg(group_id=group_id, message=f"[备份] 正在备份聊天信息...")
        database_url = config.datastore_database_url
        if "aiomysql" in database_url:
            database_url = database_url.replace("aiomysql", "pymysql")
        dataset = Dataset.from_sql("message", con=database_url)
        date = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
        commit_message = f"Auto-backup at {date}"
        dataset.push_to_hub(config.hf_repo, private=True, token=config.hf_token, commit_message=commit_message)
        at = MessageSegment.at(superuser)
        message = MessageSegment.text(f" [备份]成功备份至HuggingFace.")
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
