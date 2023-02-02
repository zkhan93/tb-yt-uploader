import logging

from telegram.ext import CommandHandler, Filters
from telegram import ParseMode

from config import get_config
from utils.common import download_audio, delete_file
from utils.service import submit_audio, get_task_status
import time

logger = logging.getLogger(__name__)


def convert(update, context):
    config = get_config()
    audio_message = update.effective_message.reply_to_message
    title = update.effective_message.text.lstrip("/convert ")
    logger.info(title)
    try:
        audio_path = download_audio(config, audio_message)
    except Exception as ex:
        logger.exception("could not extract audio file")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"error fetching audio: ```\n{str(ex)}\n```",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    else:
        try:
            task_id = submit_audio(audio_path, title=title)
        except Exception as ex:
            logger.exception("Error while submitting task")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"error submitting task: ```\n{str(ex)}\n```",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        else:
            # poll status of this task_id
            status = poll_task_status(task_id)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"uploaded: ```\n{status}\n```",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
        finally:
            delete_file(audio_path)

def poll_task_status(task_id, delay:int=3):
    res = {}
    while res.get("status") not in ("SUCCESS", "FAILURE", "REVOKED"):
        res = get_task_status(task_id)
        time.sleep(delay)
    return res



def get_convert_handler(config):
    return CommandHandler(
        "convert",
        convert,
        filters=Filters.chat(
            username=[username for username, _ in config.allowed_users]
        ),
    )
