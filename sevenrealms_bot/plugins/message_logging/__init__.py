from nonebot import require

require("nonebot_plugin_datastore")
require("nonebot_plugin_apscheduler")

import uuid

from nonebot import on
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import Depends
from nonebot.rule import Rule
from nonebot_plugin_datastore import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

from . import backup, blacklist, count
from .blacklist import get_blacklist_status
from .config import config
from .model import Message


async def message_checker(event: GroupMessageEvent):
    return str(event.group_id) in config.qq_logging_group


rule = Rule(message_checker)

matcher = on(rule=rule, priority=-1, block=False)


@matcher.handle()
async def _(event: GroupMessageEvent, session: AsyncSession = Depends(get_session)):
    user_id = event.sender.user_id
    if user_id is None:
        raise ValueError("user_id is None.")
    blacklist_status = await get_blacklist_status(user_id, session)
    sender_id = event.sender.user_id if (not blacklist_status) else 0
    nickname = (
        event.sender.nickname
        if (not (blacklist_status or event.sender.nickname == None))
        else ""
    )
    group_nickname = (
        event.sender.card
        if (not (blacklist_status or event.sender.card == None))
        else ""
    )
    message = event.get_plaintext() if not blacklist_status else ""
    raw_message = event.raw_message if not blacklist_status else ""
    message_model = Message(
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
        blacklisted=blacklist_status,
    )
    session.add(message_model)
    await session.commit()
