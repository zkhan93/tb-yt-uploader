import logging

from telegram.ext import CommandHandler, Filters
from telegram import ParseMode

from config import get_config
from utils.common import download_audio, delete_file
from utils.service import submit_audio, get_task_status
import time

logger = logging.getLogger(__name__)


def send_error(update, context, message):
    send_message(update, context, message, parse_mode=ParseMode.MARKDOWN_V2)


def send_message(update, context, message, **kwargs):
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, **kwargs)


def get_email_title(update, context):
    args = update.effective_message.text.lstrip("/convert ")
    email, title = None, None
    try:
        email, title = args.split(" ", 1)
        logger.info(f"{email} {title}")
    except Exception as ex:
        logger.exception("error parsing email and title ")
        send_error(
            update, context, f"error parsing email and/or title: ```\n{str(ex)}\n```"
        )
    return email, title


def get_download_audio_path(update, context):
    audio_message = update.effective_message.reply_to_message
    config = get_config()
    audio_path = None
    try:
        audio_path = download_audio(config, audio_message)
    except Exception as ex:
        logger.exception("error while downloading audio file")
        send_error(update, context, f"error downloading audio: ```\n{str(ex)}\n```")
    return audio_path


def submit_task(update, context, audio_path, email, title):
    task_id = None
    try:
        task_id = submit_audio(audio_path, title=title)
    except Exception as ex:
        logger.exception("Error while submitting task")
        send_error(update, context, f"error submitting task: ```\n{str(ex)}\n```")
    return task_id


def convert(update, context):

    email, title = get_email_title(update, context)
    if not email or not title:
        return

    audio_path = get_download_audio_path(update, context)
    if not audio_path:
        return

    task_id = submit_task(update, context, audio_path, email, title)
    if not task_id:
        return

    # poll status of this task_id
    status = poll_task_status(update, context, task_id)
    if not status:
        return

    send_error(update, context, f"uploaded: ```\n{status}\n```")
    delete_file(audio_path)


def poll_task_status(
    update,
    context,
    task_id,
    delay: int = 3,
):
    res = None
    try:
        while res.get("status") not in ("SUCCESS", "FAILURE", "REVOKED"):
            res = get_task_status(task_id)
            time.sleep(delay)
    except Exception as ex:
        logger.exception("Error while polling task status")
        send_error(update, context, f"error submitting task: ```\n{str(ex)}\n```")
    return res


def get_convert_handler(config):
    return CommandHandler(
        "convert",
        convert,
        filters=Filters.chat(
            username=[username for username, _ in config.allowed_users]
        ),
    )
