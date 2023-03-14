import re
import json
import uuid

from nonebot import on_message, require
from nonebot.log import logger
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from aliyunsdkalinlp.request.v20200629.GetSaChGeneralRequest import GetSaChGeneralRequest

from .alinlp import client as alinlp_client

cqreply_matcher = re.compile(r'\[CQ:reply,id=-?[0-9]+\]')


async def message_checker(event: GroupMessageEvent):
    require("sevenrealms_bot.plugins.message_logging")
    from sevenrealms_bot.plugins.message_logging.config import config
    has_reply_refer = cqreply_matcher.match(event.raw_message)
    has_command = event.raw_message.find("/情感检测") >= 0
    return has_reply_refer and str(event.group_id) in list(config.qq_logging_group) and has_command

rule = Rule(message_checker)

matcher = on_message(rule=rule, block=True)


@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import MessageEmotion, Message
    from pony import orm
    original_message_id = int(
        cqreply_matcher.match(event.raw_message)[0][13:][:-1])
    with orm.db_session:
        messages = orm.select(
            m for m in Message if m.onebot_id == original_message_id).limit(1)
        if not messages:
            await bot.send(event, "数据库中找不到该聊天内容。", reply_message=True)
            return
        selected_message: Message = messages[0]
        req = GetSaChGeneralRequest()
        req.set_ServiceCode("alinlp")
        req.set_Text(selected_message.message)
        try:
            res = alinlp_client.do_action_with_exception(req)
            res_data_obj = json.loads(res)["Data"]
            res_obj = json.loads(res_data_obj)["result"]
            positive_prob = res_obj["positive_prob"]
            negative_prob = res_obj["negative_prob"]
            neutral_prob = res_obj["neutral_prob"]
            sentiment = res_obj["sentiment"]
            sql_sentiment = "neutral"
            if sentiment == "正面":
                sql_sentiment = "positive"
            elif sentiment == "负面":
                sql_sentiment = "negative"
            await bot.send(event, f"检测结果: {sentiment}\n正面指数: {positive_prob}\n中立指数: {neutral_prob}\n负面指数: {negative_prob}", reply_message=True)
            MessageEmotion(
                uuid=str(uuid.uuid4()),
                message_uuid=selected_message.uuid,
                positive_prob=positive_prob,
                negative_prob=negative_prob,
                neutral_prob=neutral_prob,
                result=sql_sentiment
            )
        except Exception as e:
            logger.warning("ALINLP出现了问题，请查看具体情况。")
            logger.warning(e)
            await bot.send(event, f"ALINLP出现了问题，请查看具体情况。", reply_message=True)
