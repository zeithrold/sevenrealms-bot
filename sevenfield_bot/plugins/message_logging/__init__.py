from . import count
from nonebot import require, on
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import uuid
from .config import config


async def message_checker(event: GroupMessageEvent):
    return str(event.group_id) in config.qq_logging_group

rule = Rule(message_checker)

matcher = on(rule=rule)


@matcher.handle()
async def _(event: GroupMessageEvent):
    require("sevenfield_bot.plugins.db")
    from sevenfield_bot.plugins.db import Message
    from pony import orm
    with orm.db_session:
        Message(
            onebot_id=event.message_id,
            uuid=str(uuid.uuid4()),
            time=event.time,
            sender_id=event.sender.user_id,
            nickname=event.sender.nickname,
            group_nickname=event.sender.card,
            group_id=event.group_id,
            message=event.get_plaintext(),
            raw_message=event.raw_message,
            anonymous=event.anonymous is not None
        )
        orm.commit()
