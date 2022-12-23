from app.config import get_config
import base64
from cryptography.fernet import Fernet
import redis
import json
from functools import lru_cache
import google.oauth2.credentials
from contextlib import contextmanager


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


def get_cred(email) -> dict:
    r = get_redis()
    encrypted_cred = r.get(email)
    if not encrypted_cred:
        raise Exception(f"Credential not found for {email}")
    return json.loads(decrypt(encrypted_cred))


def save_cred(email, cred):
    r = get_redis()
    cred_dict = credentials_to_dict(cred)
    print("saving", cred_dict)
    encrypted_cred = encrypt(json.dumps(cred_dict))
    r.set(email, encrypted_cred)


@contextmanager
def get_credentials(email):
    credential_dic = get_cred(email)
    print("got", credential_dic)
    credentials = google.oauth2.credentials.Credentials(**credential_dic)
    try:
        yield credentials
    finally:
        save_cred(email, credentials)


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
