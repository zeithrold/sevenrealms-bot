from oss2.api import Bucket
from oss2.auth import Auth

from .config import config

auth = Auth(config.alioss_accesskey_id, config.alioss_accesskey_secret)
bucket = Bucket(auth, config.alioss_endpoint, config.alioss_bucket)
