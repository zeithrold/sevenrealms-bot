from nonebot import require

require("nonebot_plugin_datastore")
import random
from datetime import datetime

from nonebot import CommandGroup
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment
from nonebot.params import Depends
from nonebot_plugin_datastore import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import Fortune

group = CommandGroup("fortune")

main_cmd = group.command(tuple())

@main_cmd.handle()
async def generate_fortune(
    event: MessageEvent, 
    session: AsyncSession = Depends(get_session)
):
    sender_id = event.sender.user_id
    if sender_id is None:
        raise ValueError("user_id is None.")
    # Generate today string, format: YYYY-MM-DD
    today = datetime.now().strftime("%Y-%m-%d")
    # Check if today's fortune exists
    fortune = (await session.execute(select(Fortune).where(Fortune.day == today))).scalar_one_or_none()
    if fortune is None:
        fortune = Fortune(qq=sender_id, fortune=random.randint(1, 100), day=today)
        session.add(fortune)
        await session.commit()
    return_msg = f"今日运势：{fortune.fortune}"
    if event.message_type == "group":
        return_msg = MessageSegment.at(sender_id) + return_msg
    await main_cmd.finish(return_msg)
