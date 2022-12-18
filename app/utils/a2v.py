import ffmpeg


def create_video_file(audio_file: str, image_file: str, out:str):
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
        return None
    return out
