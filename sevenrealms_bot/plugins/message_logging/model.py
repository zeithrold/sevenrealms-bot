from nonebot_plugin_datastore import get_plugin_data
from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

Model = get_plugin_data().Model

class Message(Model):
    __tablename__ = "message"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    onebot_id: Mapped[int] = mapped_column("onebot_id", BigInteger)
    uuid: Mapped[str] = mapped_column("uuid", String(36))
    time: Mapped[int] = mapped_column("time", BigInteger)
    sender_id: Mapped[int] = mapped_column("sender_id", BigInteger)
    nickname: Mapped[str] = mapped_column("nickname", String(64))
    group_nickname: Mapped[str] = mapped_column("group_nickname", String(64))
    group_id: Mapped[str] = mapped_column("group_id", BigInteger)
    message: Mapped[str] = mapped_column("message", String(1024))
    raw_message: Mapped[str] = mapped_column("raw_message", String(1024))
    anonymous: Mapped[bool] = mapped_column("anonymous", Boolean)
    blacklisted: Mapped[bool] = mapped_column("blacklisted", Boolean)

class BlackList(Model):
    __tablename__ = "blacklist"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    time: Mapped[int] = mapped_column("time", BigInteger)
    uuid: Mapped[str] = mapped_column("uuid", String(36))
    status: Mapped[bool] = mapped_column("status", Boolean)
    operator_id: Mapped[int] = mapped_column("operator_id", BigInteger)

class Recall(Model):
    __tablename__ = "recall"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    recalled_onebot_id: Mapped[int] = mapped_column("recalled_onebot_id", BigInteger)
    uuid: Mapped[str] = mapped_column("uuid", String(36))
    time: Mapped[int] = mapped_column("time", BigInteger)
    sender_id: Mapped[int] = mapped_column("sender_id", BigInteger)
    operator_id: Mapped[int] = mapped_column("operator_id", BigInteger)
    group_id: Mapped[int] = mapped_column("group_id", BigInteger)

