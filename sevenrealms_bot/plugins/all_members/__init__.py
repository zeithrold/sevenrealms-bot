from nonebot import require

require("nonebot_plugin_apscheduler")
require("redis")
require("global_config")

import json
from typing import Dict

from apscheduler.triggers.cron import CronTrigger
from nonebot import get_bot, on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from nonebot_plugin_apscheduler import scheduler
from pytz import timezone
from sevenrealms_bot.plugins.global_config import global_config
from sevenrealms_bot.plugins.redis import client

from .types import AccountInfo, Group

matcher = on_command("refresh_cache", permission=SUPERUSER)


@matcher.handle()
async def handler():
    await refresh_cache()
    await matcher.finish("Cache refreshed.")


scheduled = scheduler.scheduled_job(
    CronTrigger(hour="*/12", timezone=timezone("Asia/Shanghai"))
)


async def refresh_cache():
    qq_self_id = global_config.qq_self_id
    logger.info("Refreshing cache...")
    bot: Bot = get_bot(qq_self_id)  # type: ignore
    group_list = await bot.get_group_list()
    group_list = [Group(g) for g in group_list]
    group_length = len(group_list)
    logger.debug(f"Found {group_length} groups.")
    account_list: Dict[str, AccountInfo] = {}
    for group in group_list:
        member_list = await bot.get_group_member_list(group_id=group.group_id)
        member_list = [AccountInfo(m) for m in member_list]
        member_length = len(member_list)
        logger.debug(f"Found {member_length} members in group {group.group_id}.")
        for member in member_list:
            account_list[str(member.user_id)] = member
    key_prefix = "srbot_account://"
    # delete all keys
    logger.debug("Deleting all keys...")
    keys = await client.keys(key_prefix + "*")
    for key in keys:
        await client.delete(key)
    for key in account_list:
        await client.set(key_prefix + key, json.dumps(account_list[key].__dict__))
    logger.success("Cache refreshed.")


scheduled(refresh_cache)


async def get_account_info(user_id: int) -> AccountInfo | None:
    key_prefix = "srbot_account://"
    raw = await client.get(key_prefix + str(user_id))
    if raw is None:
        return None
    return AccountInfo(json.loads(raw))
