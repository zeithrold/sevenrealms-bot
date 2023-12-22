from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from .config import config
from ghapi.all import GhApi

matcher = on_command("github")


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    api = GhApi(gh_host=config.github_api_endpoint, token=config.github_token)
    first_commit = api.repos.list_commits(owner="zeithrold", repo="sevenrealms-bot")[0]
    group_id = event.group_id
    message = MessageSegment.at(event.user_id) + MessageSegment.text(
        f" [GitHub]最近一次部署的Git Commit: {first_commit.sha[:8]}"
    )
    await bot.send_group_msg(group_id=group_id, message=message)
