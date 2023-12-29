from typing import Dict, Any

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
