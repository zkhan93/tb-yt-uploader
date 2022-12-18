import logging
import os
import time

import ffmpeg

logger = logging.getLogger(__name__)


def download_audio(config, msg):
    AUDIO_BASE = os.path.join(config.media_base, "audios")
    file = None
    if msg.voice:
        file = msg.voice.get_file()
        name = "recording.ogg"
    elif msg.audio:
        file = msg.audio.get_file()
        name = msg.audio.file_name
    else:
        raise Exception("No audio found")
    prefix = str(int(time.time()))
    audio_file_path = file.download(
        os.path.join(AUDIO_BASE, f"{prefix}_{name}"), timeout=100
    )
    return audio_file_path


def create_video_file(audio_file: str, image_file: str, out: str):
    """
    ffmpeg -y -loop 1 -i /data/img.jpg -i {file_path} -acodec copy -shortest -vf scale=1080:1920 /data/result.mp4
    """
    scale = "1080:1920"
    try:
        image = ffmpeg.input(image_file, loop=1, r=1).filter(
            "scale", size=scale, force_original_aspect_ratio="increase"
        )
        audio = ffmpeg.input(audio_file)
        (
            ffmpeg.output(image, audio, out, format="mp4", acodec="copy", shortest=None)
            .overwrite_output()
            .run()
        )
    except Exception as ex:
        logger.exception("error converting audio to video")
        return None
    return out
