import os
import logging
import tempfile
import ffmpeg
from pathlib import Path

from app.config import get_config

logger = logging.getLogger(__name__)


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


def create_video_file(audio_file: str, image_file: str):
    """
    ffmpeg -y -loop 1 -i /data/img.jpg -i {file_path} -acodec copy -shortest -vf scale=1080:1920 /data/result.mp4
    """
    scale = "1080:1920"
    ffmpeg_exception = None
    config = get_config()
    try:
        image = ffmpeg.input(image_file, loop=1, r=1).filter(
            "scale", size=scale, force_original_aspect_ratio="increase"
        )
        audio = ffmpeg.input(audio_file)
        out = None
        with tempfile.NamedTemporaryFile(delete=False, dir=config.media_base, suffix=".mp4") as video:
            print(">>>>>>>>>>>>", video.name)
            (
                ffmpeg.output(
                    image, audio, video.name, format="mp4", acodec="copy", shortest=None
                )
                .overwrite_output()
                .run(capture_stderr=True)
            )
            out = video.name
    except ffmpeg.Error as ex:
        ffmpeg_exception = ex.stderr.decode()
    else:
        Path(audio_file).unlink()
        
    if ffmpeg_exception:
        raise Exception(ffmpeg_exception)
    return out
