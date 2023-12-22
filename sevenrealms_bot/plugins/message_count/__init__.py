from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

matcher = on_command("count")


def get_count() -> int:
    require("seventield_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Message
    from pony import orm

    with orm.db_session:
        counts = orm.count(m for m in Message)
    return counts


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    counts = get_count()
    group_id = event.group_id
    message = MessageSegment.at(event.user_id) + MessageSegment.text(
        f" 目前记录的消息数量为：{counts}"
    )
    await bot.send_group_msg(group_id=group_id, message=message)
