from nonebot import on_message, require
from nonebot.rule import Rule, to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from .config import config


async def message_checker(event: GroupMessageEvent):
    require("sevenrealms_bot.plugins.global_config")
    require("sevenrealms_bot.plugins.message_logging")
    from sevenrealms_bot.plugins.message_logging.config import config as logging_config
    from sevenrealms_bot.plugins.global_config import global_config

    return (
        str(event.group_id) in logging_config.qq_logging_group
        and event.raw_message.strip() == f"[CQ:at,qq={global_config.qq_self_id}]"
    )


rule = Rule(message_checker, to_me)

matcher = on_message(rule=rule)


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    message = f"{config.about_template}"
    group_id = event.group_id
    message = MessageSegment.at(event.user_id) + MessageSegment.text(message)
    await bot.send_group_msg(group_id=group_id, message=message)
