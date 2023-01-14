from . import count
from . import scheduler
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
    require("sevenfield_bot.plugins.blacklist")
    from sevenfield_bot.plugins.blacklist import get_blacklist_status
    from sevenfield_bot.plugins.db import Message
    from pony import orm
    with orm.db_session:
        blacklist_status = get_blacklist_status(event.sender.user_id)
        sender_id = event.sender.user_id if not blacklist_status else 0
        nickname = event.sender.nickname if not blacklist_status else ""
        group_nickname = event.sender.card if not blacklist_status else ""
        message = event.get_plaintext() if not blacklist_status else ""
        raw_message = event.raw_message if not blacklist_status else ""
        Message(
            onebot_id=event.message_id,
            uuid=str(uuid.uuid4()),
            time=event.time,
            sender_id=sender_id,
            nickname=nickname,
            group_nickname=group_nickname,
            group_id=event.group_id,
            message=message,
            raw_message=raw_message,
            anonymous=event.anonymous is not None,
            blacklisted=blacklist_status
        )
        orm.commit()
