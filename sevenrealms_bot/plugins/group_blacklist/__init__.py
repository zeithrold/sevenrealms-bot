from nonebot import on_message
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from .config import config

async def message_checker(event: GroupMessageEvent):
    return str(event.group_id) in config.qq_blacklist_group

rule = Rule(message_checker)
matcher = on_message(rule=rule, priority=0)

@matcher.handle()
async def _():
    matcher.block = True
