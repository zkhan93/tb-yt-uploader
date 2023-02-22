import logging
from pathlib import Path

from celery import shared_task, Task

from app.utils.cred import check_auth_all
from app.utils.a2v import create_video_file
from app.utils.yt_uploader import upload_to_youtube
from app.utils.gmail import send_email, format_last_exception
from app.config import get_config

logger = logging.getLogger(__name__)


class BaseTask(Task):
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        send_email(f"Task {self.name} failed", format_last_exception(einfo))

class RetryingTask(BaseTask):
    autoretry_for = (Exception,)
    
class UploadRetryingTask(BaseTask):
    autoretry_for = (Exception,)
    max_retries = 24
    default_retry_delay = 3600 # an hour 


@shared_task(base=BaseTask)
def task_check_auth():
    """check access for all users, by doing so it refreshes the auth token for the user.
    if check fails raise error"""
    result = check_auth_all()
    for key, value in result.items():
        if "error" in value:
            send_email(f"token check failed {key}", f"<pre>{value}</pre>")


@shared_task(base=RetryingTask)
def task_convert_to_audio(audio_file: str, image_file: str):
    filepath = create_video_file(audio_file, image_file)
    logger.info(f"converted audio to video: {filepath}")
    return filepath


@shared_task(base=UploadRetryingTask)
def task_upload_to_youtube(filepath: str, email: str, delete=False, **kwargs):
    config = get_config()
    path = Path(filepath)
    if not path.match(config.external_pattern) or not path.is_file():
        logger.error(f"file '{filepath}' not found")
        return {"error": f"file '{filepath}' not found"}
    response = upload_to_youtube(filepath, email, delete=delete, **kwargs)
    logger.info(f"uploaded video to youtube {response}")
    return response
