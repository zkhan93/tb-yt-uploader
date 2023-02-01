import base64
import json
from functools import lru_cache
from contextlib import contextmanager
from cryptography.fernet import Fernet
import google.oauth2.credentials
import googleapiclient.discovery
import redis

from app.config import get_config


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def get_fernet():
    config = get_config()
    key = base64.b64encode(config.secret_key[:32].encode("utf-8"))
    return Fernet(key)


def encrypt(content: str):
    f = get_fernet()
    content_bytes = bytes(content, "utf-8")
    encrypted = f.encrypt(content_bytes)
    return encrypted


def decrypt(content: bytes):
    f = get_fernet()
    encrypted = f.decrypt(content)
    return encrypted


@lru_cache
def get_redis():
    config = get_config()
    return redis.Redis(host=config.redis_host, port=6379, db=0)

def _get_key(email:str):
    config = get_config()
    return f"{config.redis_key_namespace}:{email}"


def get_cred(email) -> dict:
    r = get_redis()
    encrypted_cred = r.get(_get_key(email))
    if not encrypted_cred:
        raise Exception(f"Credential not found for {email}")
    return json.loads(decrypt(encrypted_cred))


def save_cred(email, cred):
    r = get_redis()
    cred_dict = credentials_to_dict(cred)
    encrypted_cred = encrypt(json.dumps(cred_dict))
    r.set(_get_key(email), encrypted_cred)


@contextmanager
def get_credentials(email):
    credential_dic = get_cred(email)
    credentials = google.oauth2.credentials.Credentials(**credential_dic)
    try:
        yield credentials
    finally:
        save_cred(email, credentials)


def check_auth(email: str):
    with get_credentials(email) as credentials:
        service = googleapiclient.discovery.build(
            "oauth2", "v2", credentials=credentials
        )
        user_info = service.userinfo().get().execute()
        return user_info

def check_auth_all():
    r = get_redis()
    info = {}
    for key in r.scan_iter(_get_key("*")):
        _, email = key.decode().split(":")
        try:
            info[email] = check_auth(email)
        except Exception as ex:
            info[email] = {"error": str(ex)}
    return info

def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
