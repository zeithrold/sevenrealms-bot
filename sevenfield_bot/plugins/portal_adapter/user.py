from nonebot import require
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import re
from typing import List


user_app = FastAPI()


class UserMessageResponse(BaseModel):
    uuid: str
    message: str
    with_complicated_content: bool
    time: int


@user_app.get("/message/{message_uuid}")
async def get_message(message_uuid: str) -> UserMessageResponse:
    require("sevenfield_bot.plguins.db")
    from sevenfield_bot.plugins.db import Message
    from pony import orm
    with orm.db_session:
        query_result: List[Message] = orm.select(
            m for m in Message if m.uuid == message_uuid).limit(1)
    if not query_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={
                            "error": "message_not_found", "description": "requested message not found."})
    response = UserMessageResponse()
    response.uuid = message_uuid
    response.message = query_result[0].message
    pattern = re.compile(r'\[CQ:.+[,.+=.+]*\]')
    pattern_search_result = pattern.findall(pattern)
    response.with_complicated_content = False if len(
        pattern_search_result) is 0 else True
    response.time = query_result[0].time
    return response
