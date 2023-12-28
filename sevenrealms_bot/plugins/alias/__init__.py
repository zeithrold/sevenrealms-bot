from nonebot import on_command, require
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message

matcher = on_command("alias")

help_text = """参数：
/alias set <QQ号> <别名>
/alias get <QQ号>
/alias delete <QQ号>"""


@matcher.handle()
async def handle(args: Message = CommandArg()):
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
        set_alias(qq, alias)
        await matcher.finish(f"已将QQ号{qq}的别名设置为{alias}。")
    elif action == "get":
        try:
            alias = get_alias(qq)
        except ValueError:
            await matcher.finish(f"QQ号{qq}没有设置别名。")
        await matcher.finish(f"QQ号{qq}的别名为{alias}。")
    elif action == "delete":
        try:
            delete_alias(qq)
        except ValueError:
            await matcher.finish(f"QQ号{qq}没有设置别名。")
        await matcher.finish(f"已删除QQ号{qq}的别名。")
    else:
        await matcher.finish(help_text)


def get_alias(qq: int):
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Alias
    from pony import orm

    with orm.db_session:
        counts = orm.select(a for a in Alias if a.qq == qq).count()
        if counts >= 1:
            latest_alias = orm.select(a for a in Alias if a.qq == qq).limit(1)[0]
            current_alias = latest_alias.alia
        else:
            current_alias = None
    return current_alias


def set_alias(qq: int, alias: str) -> None:
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Alias
    from pony import orm

    with orm.db_session:
        alias_query = orm.select(a for a in Alias if a.qq == qq)
        exists = alias_query.count() >= 1
        if exists:
            alias_objs = alias_query[:]
            for a in alias_objs:
                a.alias = alias
        else:
            Alias(qq=qq, alia=alias)
        orm.commit()

def delete_alias(qq: int) -> None:
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Alias
    from pony import orm

    with orm.db_session:
        alias_query = orm.select(a for a in Alias if a.qq == qq)
        exists = alias_query.count() >= 1
        if exists:
            alias_query.delete()
            orm.commit()
        else:
            raise ValueError("No alias found.")
