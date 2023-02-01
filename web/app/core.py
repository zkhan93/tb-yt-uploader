import logging

from fastapi import APIRouter, Request, Depends, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
import googleapiclient.discovery
from pydantic import BaseModel
from celery.result import AsyncResult
from app.config import Settings, get_config
from app.utils.cred import get_credentials
from app.tasks import task_convert_to_audio, task_upload_to_youtube

logger = logging.getLogger(__name__)


core = APIRouter()

@core.get("/test")
async def test(request: Request, config: Settings = Depends(get_config)):
    try:
        with get_credentials(config.youtube_email) as credentials:
            # Load credentials from the session.
            service = googleapiclient.discovery.build(
                "oauth2", "v2", credentials=credentials
            )
            user_info = service.userinfo().get().execute()
    except Exception as ex:
        logger.exception(ex)
        return RedirectResponse("/authorize")
    else:
        return user_info
def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result

@core.get("/task/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    return get_task_info(task_id)

@core.post("/convert-and-upload-to-youtube")
async def convert_and_upload(audio: UploadFile):
    # take a video file
    # create task to convert audio to video
    # that task after completion should start the task to upload the converted video    
    src_audio_path = audio.filename
    dst_video = "test.mp4"
    src_image = ""
    print(audio.filename)
    task = task_convert_to_audio.apply_async(args=[src_audio_path, src_image, dst_video])
    return JSONResponse({"task_id": task.id})

class Status(BaseModel):
    selfDeclaredMadeForKids:bool = False
    privacyStatus: str = "public"

class Snippet(BaseModel):
    title:str = "New Video"
    tags:list[str] = ["islamic"]
    categoryId:list[str] = ["22"]

class VideoInfo(BaseModel):
    snippet: Snippet
    status: Status

@core.post("/upload-to-youtube")
async def upload_to_youtube(video: UploadFile, info: Snippet):
    # take a video file
    # save it on disk
    # add task to upload it to youtube (task should clean up after upload)
    extras = info.dict()
    print(video.filename)
    task_upload_to_youtube.apply_async(args=[video.filename], kwargs=extras)
