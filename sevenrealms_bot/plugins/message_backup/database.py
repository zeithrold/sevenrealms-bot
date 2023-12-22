from nonebot import require
import pandas as pd
import tempfile
import os
import os.path
import py7zr
import time
import uuid
from pony import orm
from .config import config


def generate_dataset():
    temp_dir: str = tempfile.gettempdir()
    folder_uuid = str(uuid.uuid4())
    data_dir = f"{temp_dir}/data-{folder_uuid}"
    os.mkdir(data_dir)
    current_time_struct = time.localtime()
    year = current_time_struct.tm_year
    month = "%02d" % current_time_struct.tm_mon
    day = "%02d" % current_time_struct.tm_mday
    time_limit = int(
        time.mktime(
            time.strptime(
                f"{current_time_struct.tm_year} {current_time_struct.tm_mon} {current_time_struct.tm_mday}",
                "%Y %m %d",
            )
        )
    )
    require("sevenrealms_bot.plugins.db")
    from sevenrealms_bot.plugins.db import Message, Recall

    with orm.db_session:
        result = Message.select(
            lambda m: (
                not (
                    m.blacklisted
                    or m.anonymous
                    or orm.exists(
                        recall
                        for recall in Recall
                        if recall.recalled_onebot_id == m.onebot_id
                    )
                )
            )
            and m.time <= time_limit
        )
        df_array = []
        for r in result:
            df_array.append(r.to_dict())

    df = pd.DataFrame(df_array)
    df.set_index("id", drop=True, inplace=True)
    data_file_name = "data.csv"
    data_full_path = f"{data_dir}/{data_file_name}"
    df.to_csv(data_full_path)
    archive_file_name = f"data_{year}{month}{day}.7z"
    archive_full_path = f"{temp_dir}/{archive_file_name}"
    with py7zr.SevenZipFile(
        archive_full_path, "w", password=config.alioss_encrypt_password
    ) as f:
        f.write(data_full_path, arcname=data_file_name)
    os.remove(data_full_path)
    return archive_full_path, archive_file_name
