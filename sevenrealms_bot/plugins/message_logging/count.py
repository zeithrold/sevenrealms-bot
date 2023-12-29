from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.params import Depends
from nonebot_plugin_datastore import get_session
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import Message

matcher = on_command("count")


async def get_count(session: AsyncSession) -> int:
    counts = (await session.execute(select(func.count(Message.id)))).scalar_one()
    return counts


@matcher.handle()
async def _(session: AsyncSession = Depends(get_session)):
    counts = await get_count(session)
    message = MessageSegment.text(f" 目前记录的消息数量为：{counts}")
    await matcher.finish(message)
