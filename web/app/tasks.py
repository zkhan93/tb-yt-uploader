import logging

from celery import shared_task

from app.utils.cred import check_auth_all
from app.utils.a2v import create_video_file
from app.utils.yt_uploader import upload_to_youtube


logger = logging.getLogger(__name__)


@shared_task()
def task_check_auth():
    """check access for all users, by doing so it refreshes the auth token for the user.
    if check fails raise error"""
    return check_auth_all()


@shared_task()
def task_convert_to_audio(audio_file: str, image_file: str):
    filepath = create_video_file(audio_file, image_file)
    logger.info(f"converted audio to video: {filepath}")
    return filepath


@shared_task()
def task_upload_to_youtube(filepath: str, email: str, **kwargs):
    response = upload_to_youtube(filepath, email, **kwargs)
    return response
