import os
import time
import logging

from telegram import Update
from telegram.ext.utils.types import CCT
from telegram.ext import MessageHandler, Filters

from app.config import get_config
from app.utils.yt_uploader import upload_to_youtube
from app.utils.a2v import create_video_file
import whisper

logger = logging.getLogger(__name__)


def audio2video(update: Update, context: CCT):
    config = get_config()
    IMAGE_PATH = os.path.join(config.media_base, "images", "img.jpg")
    AUDIO_BASE = os.path.join(config.media_base, "audios")
    VIDEO_PATH = os.path.join(config.media_base, "videos", "result.mp4")
    logger.info(update.effective_message)
    file = None
    if update.effective_message.voice:
        file = update.effective_message.voice.get_file()
        name = "recording.ogg"
    if update.effective_message.audio:
        file = update.effective_message.audio.get_file()
        name = update.effective_message.audio.file_name
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="downloading audio message",
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="audio detected",
    )
    prefix = str(int(time.time()))
    logger.debug(f"{prefix}_{name}")
    audio_file_path = file.download(
        os.path.join(AUDIO_BASE, f"{prefix}_{name}"), timeout=100
    )
    logger.debug(f"file saved at {audio_file_path}")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="file downloaded, creating video...",
    )
    video_path = create_video_file(audio_file_path, IMAGE_PATH, VIDEO_PATH)
    context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open(video_path, "rb"),
        caption="video created, uploading to youtube..",
    )
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)
    except Exception as ex:
        description = ""
    else:
        description = result["text"]
    try:
        upload_to_youtube(video_path, description)
    except Exception as ex:
        logger.exception("Error while uploading to youtube")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"error uploading: {str(ex)}",
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="uploading complete",
        )

def get_handler(config):
    return MessageHandler(
        Filters.voice | Filters.audio,
        audio2video,
    )
