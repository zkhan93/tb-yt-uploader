from celery import shared_task
from app.config import get_config
import logging

from app.utils.cred import get_credentials
from app.utils.a2v import create_video_file
from app.utils.yt_uploader import upload_to_youtube
import googleapiclient.discovery

logger = logging.getLogger(__name__)

@shared_task()
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

@shared_task()
def task_convert_to_audio(audio_file: str, image_file: str, out: str):
    create_video_file(audio_file, image_file, out)

@shared_task()
def task_upload_to_youtube(filepath:str, **kwargs):
    upload_to_youtube(filepath, **kwargs)
