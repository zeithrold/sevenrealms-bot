from nonebot import on_command, require
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message
from typing import List

matcher = on_command("group")

help_text = """参数：
/group set <QQ号> <群组ID>
/group delete <QQ号> <群组ID>
/group get <QQ号>
/group list <群组ID> (需要在群聊中使用)
"""


@matcher.handle()
async def handle(args: Message = CommandArg()):
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
            set_group(qq, group_id)
        except ValueError:
            await matcher.finish("群组已存在。")
        await matcher.finish(f"已将QQ号{qq}添加到群组{group_id}。")
    elif action == "get":
        try:
            groups = get_group(qq)
        except ValueError:
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
        delete_group(qq, group_id)
        await matcher.finish(f"已将QQ号{qq}从群组{group_id}中删除。")
    elif action == "list":
        try:
            group_id = splited_params[1]
        except IndexError:
            await matcher.finish(help_text)
        require("sevenrealms_bot.plugins.all_members")
        require("sevenrealms_bot.plugins.alias")
        from sevenrealms_bot.plugins.all_members import get_account_info
        from sevenrealms_bot.plugins.alias import get_alias

        members = list_group(group_id)
        logger.info(members)
        usernames: List[str] = []
        for member in members:
            account_info = get_account_info(member)
            alias = get_alias(member)
            if alias is not None:
                usernames.append(f"{alias} ({member})")
            elif account_info is not None:
                usernames.append(f"{account_info.nickname} ({member})")
            else:
                usernames.append(f"未知用户 ({member})")
        return_str = f"群组{group_id}的成员为：\n"
        return_str += "\n".join(usernames)
        await matcher.finish(return_str)


def set_group(qq: int, group_id: str):
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import MemberGroup
    from pony import orm

    with orm.db_session:
        counts = orm.select(
            a for a in MemberGroup if a.qq == qq and a.group_id == group_id
        ).count()
        if counts >= 1:
            raise ValueError("Group already exists.")
        MemberGroup(qq=qq, group_id=group_id)
        orm.commit()


def delete_group(qq: int, group_id: str):
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import MemberGroup
    from pony import orm

    with orm.db_session:
        counts = orm.select(
            a for a in MemberGroup if a.qq == qq and a.group_id == group_id
        ).count()
        if counts >= 1:
            orm.select(
                a for a in MemberGroup if a.qq == qq and a.group_id == group_id
            ).delete()
            orm.commit()
        else:
            raise ValueError("Group not found.")


def get_group(qq: int) -> list[str]:
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import MemberGroup
    from pony import orm

    with orm.db_session:
        counts = orm.select(a for a in MemberGroup if a.qq == qq).count()
        if counts >= 1:
            groups = orm.select(a for a in MemberGroup if a.qq == qq)[:]
            result = [g.group_id for g in groups]
        else:
            raise ValueError("No group found.")
    return result


def list_group(group_id: str) -> list[int]:
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import MemberGroup
    from pony import orm

    with orm.db_session:
        counts = orm.select(a for a in MemberGroup if a.group_id == group_id).count()
        if counts >= 1:
            members = orm.select(a for a in MemberGroup if a.group_id == group_id)[:]
            result = [m.qq for m in members]
        else:
            raise ValueError("No member found.")
    return result
