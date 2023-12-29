from nonebot import require

require("nonebot_plugin_datastore")
require("all_members")
require("alias")
from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger
from nonebot.params import CommandArg, Depends
from nonebot.permission import SUPERUSER
from nonebot_plugin_datastore import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import MemberGroup

matcher = on_command("group", permission=SUPERUSER)

help_text = """参数：
/group set <QQ号> <群组ID>
/group delete <QQ号> <群组ID>
/group get <QQ号>
/group list <群组ID> (需要在群聊中使用)
"""


@matcher.handle()
async def handle(
    args: Message = CommandArg(), session: AsyncSession = Depends(get_session)
):
    param = args.extract_plain_text()
    if not param:
        await matcher.finish(help_text)
    splited_params = param.split(" ")
    action = splited_params[0]
    if action == "set":
        try:
            qq = int(splited_params[1])
            group_id = splited_params[2]
        except ValueError:
            await matcher.finish("QQ号必须是数字。")
        except IndexError:
            await matcher.finish(help_text)
        try:
            await set_group(qq, group_id, session)
        except ValueError:
            await matcher.finish("群组已存在。")
        await matcher.finish(f"已将QQ号{qq}添加到群组{group_id}。")
    elif action == "get":
        try:
            qq = int(splited_params[1])
            groups = await get_group(qq, session)
        except IndexError:
            await matcher.finish(help_text)
        except ValueError:
            qq = int(splited_params[1])
            await matcher.finish(f"QQ号{qq}没有设置群组。")
        return_str = f"QQ号{qq}的群组为：\n"
        return_str += "\n".join(groups)
        await matcher.finish(return_str)
    elif action == "delete":
        try:
            qq = int(splited_params[1])
            group_id = splited_params[2]
        except ValueError:
            await matcher.finish("QQ号必须是数字。")
        except IndexError:
            await matcher.finish(help_text)
        await delete_group(qq, group_id, session)
        await matcher.finish(f"已将QQ号{qq}从群组{group_id}中删除。")
    elif action == "list":
        try:
            group_id = splited_params[1]
        except IndexError:
            await matcher.finish(help_text)
        from sevenrealms_bot.plugins.alias import get_alias
        from sevenrealms_bot.plugins.all_members import get_account_info
        try:
            members = await list_group(group_id, session)
        except ValueError:
            await matcher.finish('找不到群组。')
        logger.info(members)
        usernames: List[str] = []
        for member in members:
            account_info = await get_account_info(member)
            alias = await get_alias(member, session)
            if alias is not None:
                usernames.append(f"{alias} ({member})")
            elif account_info is not None:
                usernames.append(f"{account_info.nickname} ({member})")
            else:
                usernames.append(f"未知用户 ({member})")
        return_str = f"群组{group_id}的成员为：\n"
        return_str += "\n".join(usernames)
        await matcher.finish(return_str)
    else:
        await matcher.finish(help_text)


async def set_group(qq: int, group_id: str, session: AsyncSession):
    member = (
        await session.execute(
            select(MemberGroup)
            .where(MemberGroup.qq == qq)
            .where(MemberGroup.group_id == group_id)
        )
    ).scalar_one_or_none()
    if member is None:
        member = MemberGroup(qq=qq, group_id=group_id)
        session.add(member)
        await session.commit()
    else:
        raise ValueError("Group already exists.")


async def delete_group(qq: int, group_id: str, session: AsyncSession):
    groups = (
        (
            await session.execute(
                select(MemberGroup)
                .where(MemberGroup.qq == qq)
                .where(MemberGroup.group_id == group_id)
            )
        )
        .scalars()
        .all()
    )
    if len(groups) >= 1:
        for group in groups:
            await session.delete(group)
        await session.commit()
    else:
        raise ValueError("Group not found.")


async def get_group(qq: int, session: AsyncSession) -> list[str]:
    group = (
        (await session.execute(select(MemberGroup).where(MemberGroup.qq == qq)))
        .scalars()
        .all()
    )
    if len(group) >= 1:
        result = [g.group_id for g in group]
        return result
    raise ValueError("No group found.")


async def list_group(group_id: str, session: AsyncSession) -> list[int]:
    group = (
        (
            await session.execute(
                select(MemberGroup).where(MemberGroup.group_id == group_id)
            )
        )
        .scalars()
        .all()
    )
    if len(group) >= 1:
        result = [g.qq for g in group]
        return result
    raise ValueError("No member found.")
