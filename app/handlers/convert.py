import os
import logging

from telegram.ext import CommandHandler, Filters
from telegram import ParseMode

from app.config import get_config
from app.utils.a2v import create_video_file, download_audio, delete_file
from app.utils.yt_uploader import upload_to_youtube

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
        IMAGE_PATH = os.path.join(config.media_base, "images", "img.jpg")
        VIDEO_PATH = os.path.join(config.media_base, "videos", "result.mp4")
        try:
            video_path = create_video_file(audio_path, IMAGE_PATH, VIDEO_PATH)
        except Exception as ex:
            logger.exception("error creating video file")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"error creating video: ```\n{str(ex)}\n```",
                parse_mode=ParseMode.MARKDOWN_V2,
            )
            delete_file(audio_path)
        else:
            try:
                result = upload_to_youtube(video_path, title=title)
            except Exception as ex:
                logger.exception("Error while uploading to youtube")
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"error uploading video: ```\n{str(ex)}\n```",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            else:
                context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=open(video_path, "rb"),
                    caption=f"uploaded: ```\n{result}\n```",
                    parse_mode=ParseMode.MARKDOWN_V2,
                )
            finally:
                delete_file(audio_path)
                delete_file(video_path)


def get_convert_handler(config):
    return CommandHandler(
        "convert",
        convert,
        filters=Filters.chat(
            username=[username for username, _ in config.allowed_users]
        ),
    )
