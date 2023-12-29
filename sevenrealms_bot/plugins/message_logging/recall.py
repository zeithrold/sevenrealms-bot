import uuid

from nonebot import on_notice
from nonebot.adapters.onebot.v11 import GroupRecallNoticeEvent
from nonebot.params import Depends
from nonebot.rule import Rule
from nonebot_plugin_datastore import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

from .config import config
from .model import Recall


async def notice_checker(event: GroupRecallNoticeEvent):
    return str(event.group_id) in config.qq_logging_group


rule = Rule(notice_checker)
matcher = on_notice(rule=rule)


@matcher.handle()
async def _(
    event: GroupRecallNoticeEvent, session: AsyncSession = Depends(get_session)
):
    recall = Recall(
        recalled_onebot_id=event.message_id,
        uuid=str(uuid.uuid4()),
        time=event.time,
        sender_id=event.user_id,
        operator_id=event.operator_id,
        group_id=event.group_id,
    )
    session.add(recall)
    await session.commit()
