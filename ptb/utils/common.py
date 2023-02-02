import logging
import os
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def download_audio(config, msg):
    file = None
    if msg.voice:
        file = msg.voice.get_file()
        name = "recording.ogg"
    elif msg.audio:
        file = msg.audio.get_file()
        name = msg.audio.file_name
    else:
        raise Exception("No audio found")
    audio_file = None
    with NamedTemporaryFile(delete=False, dir=config.media_base, suffix=name) as audio_fh:
        file.download(
            out=audio_fh, timeout=100
        )
        audio_file = audio_fh.name
    print(">>>>>>>>>>>>Saved", audio_file)
    return audio_file

