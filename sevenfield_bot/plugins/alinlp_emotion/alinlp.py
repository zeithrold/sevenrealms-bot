from .config import config

from aliyunsdkcore.client import AcsClient

client = AcsClient(
    config.alinlp_accesskey_id,
    config.alinlp_accesskey_secret,
)

