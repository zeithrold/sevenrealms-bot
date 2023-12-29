from nonebot_plugin_datastore import get_plugin_data
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

Model = get_plugin_data().Model

class Alias(Model):
    __tablename__ = "alias"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    qq: Mapped[int] = mapped_column("qq", BigInteger)
    alias: Mapped[str] = mapped_column("alias", String(64))
