import os
import os.path
import tempfile
import time
import uuid

import pandas as pd
import py7zr
from nonebot.log import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from tqdm import tqdm

from .config import config
from .model import Message, Recall


async def get_dict(message: Message, session: AsyncSession):
    is_recalled = (
        await session.execute(
            select(Recall).where(Recall.recalled_onebot_id == message.onebot_id)
        )
    ).scalar_one_or_none() is not None
    if is_recalled:
        return None
    message_dict = dict(message.__dict__)
    message_dict.pop("_sa_instance_state", None)
    return message_dict

async def generate_dataset(session: AsyncSession):
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
    logger.info('Quering Database for messages...')
    messages = (
        (
            await session.execute(
                select(Message)
                .where(Message.blacklisted == False)
                .where(Message.anonymous == False)
                .where(Message.time <= time_limit)
            )
        )
        .scalars()
        .all()
    )
    logger.info('Quering Database for recalls...')
    recalls = (await session.execute(select(Recall))).scalars().all()
    recalled_onebot_id = [r.recalled_onebot_id for r in recalls]
    messages_array = []
    for message in tqdm(messages):
        is_recalled = message.onebot_id in recalled_onebot_id
        if is_recalled:
            continue
        message_dict = dict(message.__dict__)
        message_dict.pop("_sa_instance_state", None)
        messages_array.append(message_dict)
    df = pd.DataFrame(messages_array)
    data_file_name = "data.csv"
    data_full_path = f"{data_dir}/{data_file_name}"
    archive_file_name = f"data_{year}{month}{day}.7z"
    archive_full_path = f"{temp_dir}/{archive_file_name}"
    logger.info(f'Saving to {archive_file_name}...')
    df.to_csv(data_full_path)
    with py7zr.SevenZipFile(
        archive_full_path, "w", password=config.alioss_encrypt_password
    ) as f:
        f.write(data_full_path, arcname=data_file_name)
    os.remove(data_full_path)
    logger.success('File export success.')
    return archive_full_path, archive_file_name
