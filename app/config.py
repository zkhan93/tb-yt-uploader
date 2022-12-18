from pydantic import BaseSettings
from typing import Any
import base64
import json
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    media_base: str
    token: str
    allowed_users: list[tuple]
    client_secret_json: dict
    oauth_redirect_uri: str
    secret_key: str
    redis_host: str
    youtube_email: str

    class Config:
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str) -> Any:
            if field_name == "allowed_users":
                return [tuple(x.strip().split(':')) for x in raw_val.split(",")]
            if field_name == "client_secret_json":
                return json.loads(base64.b64decode(raw_val))
            return cls.json_loads(raw_val)

@lru_cache
def get_config():
    config = Settings()
    return config
