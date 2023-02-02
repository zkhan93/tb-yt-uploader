from config import get_config
from pathlib import Path
import requests


def submit_audio(audio: Path, **kwargs):
    """ http call to the our website website 
        curl -X 'POST' \
        'http://localhost:8080/convert-and-upload-to-youtube?title=New%20Video' \
        -H 'accept: application/json' \
        -H 'access_token: 123456' \
        -H 'Content-Type: multipart/form-data' \
        -F 'audio=@file_example_MP3_700KB.mp3;type=audio/mpeg' \
        -F 'email=zkhan1093@gmail.com' \
        -F 'image=' \
        -F 'tags=islamic' \
        -F 'categoryId=22'
    """
    config = get_config()
    res = requests.post(
        "http://web/convert-and-upload-to-youtube",
        params=dict(title=kwargs.get("title", "New Video")),
        headers={"access_token": config.access_token},
        files={"audio": open(audio, "rb")},
        data=dict(
            email="zkhan1093@gmail.com", image=None, tags="islamic", categoryId=22
        ),
    )
    data = res.json()
    print(data)
    return data["task_id"]


def submit_video(video: Path, **kwargs):
    """
    curl -X 'POST' \
  'http://localhost:8080/upload-to-youtube?title=New%20Video' \
  -H 'accept: application/json' \
  -H 'access_token: 123456' \
  -H 'Content-Type: multipart/form-data' \
  -F 'video=@tmpt59v6efq.mp4;type=video/mp4' \
  -F 'email=zkhan1093@gmail.com' \
  -F 'tags=music' \
  -F 'categoryId=22'
    """
    config = get_config()
    res = requests.post(
        "http://web/upload-to-youtube",
        params=dict(title=kwargs.get("title", "New Video")),
        headers={"access_token": config.access_token},
        files={"video": open(video, "rb")},
        data=dict(
            email="zkhan1093@gmail.com", image=None, tags="islamic", categoryId=22
        ),
    )
    data = res.json()
    print(data)
    return data["task_id"]


def get_task_status(task_id: str):
    """ make call to api to get status
    curl -X 'GET' \
  'http://localhost:8080/task/b871c6da-54c7-4efa-b4b8-02f81ec5609f' \
  -H 'accept: application/json' \
  -H 'access_token: 123456'
    """
    config = get_config()
    res = requests.get(
        f"http://web/task/{task_id}",
        headers={"access_token": config.access_token},
    )
    data = res.json()
    print(data)
    return data
