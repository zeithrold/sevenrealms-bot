from .config import config
from pony import orm

db = orm.Database()

class Message(db.Entity):
    onebot_id = orm.Required(int, size=64)
    uuid = orm.Required(str, max_len=36)
    time = orm.Required(int, size=64)
    sender_id = orm.Required(int, size=64)
    nickname = orm.Required(str, max_len=64)
    group_nickname = orm.Optional(str, max_len=64)
    group_id = orm.Required(int, size=64)
    message = orm.Optional(str, max_len=1024)
    raw_message = orm.Optional(str, max_len=1024)
    anonymous = orm.Required(bool)

class Lifecycle(db.Entity):
    time = orm.Required(float)
    type = orm.Required(str, 16)

db.bind(provider='mysql',
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        passwd=config.mysql_password,
        db=config.mysql_database,
        charset='utf8mb4'
)
db.generate_mapping(create_tables=True)
