from nonebot import on_message
from nonebot.rule import Rule, to_me
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from .config import config
from ghapi.all import GhApi


async def message_checker(event: GroupMessageEvent):
    return event.get_plaintext() == "git"

rule = Rule(message_checker, to_me)

matcher = on_message(rule=rule)

@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    api = GhApi(gh_host=config.github_api_endpoint, token=config.github_access_token)
    first_commit = api.repos.list_commits(owner="zeithrold", repo="sevenfield-bot")[0]
    await bot.send_group_msg(group_id=event.group_id, message=f"[CQ:reply,id={event.message_id}] [GitHub]最近一次部署的Git Commit: {first_commit.sha[:8]}")
