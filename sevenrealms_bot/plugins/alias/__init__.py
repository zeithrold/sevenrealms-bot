from nonebot import require

require("nonebot_plugin_datastore")

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg, Depends
from nonebot.permission import SUPERUSER
from nonebot_plugin_datastore import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import Alias

matcher = on_command("alias", permission=SUPERUSER)

help_text = """参数：
/alias set <QQ号> <别名>
/alias get <QQ号>
/alias delete <QQ号>"""


@matcher.handle()
async def handle(
    args: Message = CommandArg(), session: AsyncSession = Depends(get_session)
):
    param = args.extract_plain_text()
    if not param:
        await matcher.finish(help_text)
    splited_params = param.split(" ")
    action = splited_params[0]
    try:
        qq = int(splited_params[1])
    except ValueError:
        await matcher.finish("QQ号必须是数字。")
    except IndexError:
        await matcher.finish(help_text)
    if action == "set":
        try:
            alias = splited_params[2]
        except IndexError:
            await matcher.finish(help_text)
        await set_alias(qq, alias, session)
        await matcher.finish(f"已将QQ号{qq}的别名设置为{alias}。")
    elif action == "get":
        try:
            alias = await get_alias(qq, session)
        except ValueError:
            await matcher.finish(f"QQ号{qq}没有设置别名。")
        await matcher.finish(f"QQ号{qq}的别名为{alias}。")
    elif action == "delete":
        try:
            await delete_alias(qq, session)
        except ValueError:
            await matcher.finish(f"QQ号{qq}没有设置别名。")
        await matcher.finish(f"已删除QQ号{qq}的别名。")
    else:
        await matcher.finish(help_text)


async def get_alias(qq: int, session: AsyncSession):
    alias = (
        await session.execute(select(Alias).where(Alias.qq == qq))
    ).scalar_one_or_none()
    if alias is None:
        raise ValueError("No alias found.")
    return alias.alias


async def set_alias(qq: int, alias: str, session: AsyncSession):
    alias_obj = (
        await session.execute(select(Alias).where(Alias.qq == qq))
    ).scalar_one_or_none()
    if alias_obj is None:
        alias_obj = Alias(qq=qq, alias=alias)
        session.add(alias_obj)
    else:
        alias_obj.alias = alias
    await session.commit()


async def delete_alias(qq: int, session: AsyncSession) -> None:
    alias_obj = (
        await session.execute(select(Alias).where(Alias.qq == qq))
    ).scalar_one_or_none()
    if alias_obj is None:
        raise ValueError("No alias found.")
    await session.delete(alias_obj)
    await session.commit()
