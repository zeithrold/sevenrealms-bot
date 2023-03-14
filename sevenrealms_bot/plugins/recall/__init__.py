from nonebot import on_notice, require
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import GroupRecallNoticeEvent
import uuid

async def notice_checker(event: GroupRecallNoticeEvent):
    require("sevenrealms_bot.plugins.message_logging")
    from sevenrealms_bot.plugins.message_logging import config
    return str(event.group_id) in config.qq_logging_group

rule = Rule(notice_checker)
matcher = on_notice(rule=rule)

@matcher.handle()
async def _(event: GroupRecallNoticeEvent):
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Recall
    from pony import orm
    with orm.db_session:
        Recall(
            recalled_onebot_id=event.message_id,
            uuid=str(uuid.uuid4()),
            time=event.time,
            sender_id=event.user_id,
            operator_id=event.operator_id,
            group_id=event.group_id
        )
        orm.commit()
