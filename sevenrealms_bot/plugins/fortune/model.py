from nonebot_plugin_datastore import get_plugin_data
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

Model = get_plugin_data().Model

class Fortune(Model):
    __tablename__ = "fortune"
    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    qq: Mapped[int] = mapped_column("qq", BigInteger)
    fortune: Mapped[int] = mapped_column("fortune", BigInteger)
    day: Mapped[str] = mapped_column("day", String(20))