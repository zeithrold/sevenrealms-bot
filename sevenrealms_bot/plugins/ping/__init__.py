from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

matcher = on_command("ping")


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    print(event)
    print(bot)
    group_id = event.group_id
    reply = MessageSegment.at(event.user_id) + MessageSegment.text(" pong")
    await bot.send_group_msg(group_id=group_id, message=reply)
