from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

matcher = on_command("ping")


@matcher.handle()
async def _():
    await matcher.finish(MessageSegment.text("Pong!"))
