from nonebot_plugin_datastore import get_plugin_data
from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

Model = get_plugin_data().Model

class MemberGroup(Model):
    __tablename__ = "membergroup"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    qq: Mapped[int] = mapped_column("qq", BigInteger)
    group_id: Mapped[str] = mapped_column("group_id", String(64))
