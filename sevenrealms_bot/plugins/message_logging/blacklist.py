import uuid

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from nonebot.params import Depends
from nonebot.rule import Rule
from nonebot_plugin_datastore import get_session
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio.session import AsyncSession

from .model import BlackList


async def command_checker(event: GroupMessageEvent):
    return event.raw_message.strip() in ["/blacklist", "/blacklist toggle"]


rule = Rule(command_checker)

matcher = on_command("blacklist", rule=rule)


async def get_blacklist_status(operator_id: int, session: AsyncSession) -> bool:
    current_status = False

    counts = (
        await session.execute(
            select(func.count(BlackList.id)).where(BlackList.operator_id == operator_id)
        )
    ).scalar_one()
    if counts >= 1:
        latest_blacklist_log = (
            await session.execute(
                select(BlackList)
                .where(BlackList.operator_id == operator_id)
                .order_by(BlackList.time.desc())
                .limit(1)
            )
        ).scalar_one()
        current_status = latest_blacklist_log.status
    return current_status


class BlacklistParam:
    def __init__(
        self,
        operator_id: int,
        current_status: bool,
        command_name: str,
        message_id: int,
        time: int,
        group_id: int,
    ) -> None:
        self.operator_id = operator_id
        self.current_status = current_status
        self.command_name = command_name
        self.message_id = message_id
        self.time = time
        self.group_id = group_id


async def depend(event: GroupMessageEvent, session: AsyncSession = Depends(get_session)):
    command_name = "status" if event.raw_message.strip() == "/blacklist" else "toggle"
    operator_id = event.user_id
    message_id = event.message_id
    time = event.time
    current_status = await get_blacklist_status(operator_id, session)
    group_id = event.group_id
    return BlacklistParam(
        operator_id, current_status, command_name, message_id, time, group_id
    )


@matcher.handle()
async def _(
    bot: Bot,
    param: BlacklistParam = Depends(depend),
    session: AsyncSession = Depends(get_session),
):
    if param.command_name == "status":
        at = MessageSegment.at(param.operator_id)
        message = MessageSegment.text(
            f"\n您的目前聊天记录收集黑名单状态为：{'开启' if param.current_status else '关闭'}"
            "\n"
            f"小小Z将{'不会' if param.current_status else '会'}收集您的聊天记录信息。"
            f"{'为保证数据集完整性，小小Z将用抹去QQ号码、昵称、群名片与聊天内容的空白占位符替代聊天信息记录。' if param.current_status else ''}"
            "\n"
            f"您可以通过输入 /blacklist toggle 以{'关闭' if param.current_status else '打开'}您的黑名单状态。"
        )
        await bot.send_group_msg(group_id=param.group_id, message=(at + message))
    else:
        toggled_status = not param.current_status
        blacklist = BlackList(
            time=param.time,
            uuid=str(uuid.uuid4()),
            status=toggled_status,
            operator_id=param.operator_id,
        )
        session.add(blacklist)
        await session.commit()
        at = MessageSegment.at(param.operator_id)
        message = MessageSegment.text(
            f"\n您已将您的黑名单状态更改为：{'开启' if toggled_status else '关闭'}"
            "\n"
            f"小小Z将{'不会' if toggled_status else '会'}收集您的聊天记录信息。"
            f"{'为保证数据集完整性，小小Z将用抹去QQ号码、昵称、群名片与聊天内容的空白占位符替代聊天信息记录。' if toggled_status else ''}"
            "\n"
            f"您可以通过输入 /blacklist toggle 以{'关闭' if toggled_status else '打开'}您的黑名单状态。"
        )
        await bot.send_group_msg(group_id=param.group_id, message=(at + message))
