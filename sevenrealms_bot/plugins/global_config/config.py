from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    qq_self_id: str
    qq_main_group: str
