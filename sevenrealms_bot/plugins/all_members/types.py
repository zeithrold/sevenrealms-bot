from typing import Dict, Any

# class GroupMemberInfo:
#     group_id: int
#     user_id: int
#     nickname: str
#     card: str | None
#     sex: str
#     age: int
#     area: str
#     join_time: int
#     last_sent_time: int
#     level: str
#     role: str
#     unfriendly: bool
#     title: str
#     title_expire_time: int
#     card_changeable: bool
#     def __init__(self, raw: Dict[str, Any]) -> None:
#         self.__dict__ = raw

class AccountInfo:
    user_id: int
    nickname: str
    sex: str
    age: int
    level: str
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.__dict__ = raw

class Group:
    group_id: int
    group_name: str
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.__dict__ = raw
