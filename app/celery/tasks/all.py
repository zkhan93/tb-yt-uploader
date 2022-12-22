from app.celery import app
from app.config import get_config
import logging

from app.utils.cred import get_credentials
import googleapiclient.discovery

logger = logging.getLogger(__name__)

@app.task
def check_auth():
    config = get_config()
    try:
        with get_credentials(config.youtube_email) as credentials:
            # Load credentials from the session.
            service = googleapiclient.discovery.build(
                "oauth2", "v2", credentials=credentials
            )
            user_info = service.userinfo().get().execute()
    except Exception as ex:
        logger.exception(ex)
    else:
        logger.info(user_info)
