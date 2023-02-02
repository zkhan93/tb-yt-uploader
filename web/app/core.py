import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil

from fastapi import APIRouter, Depends, UploadFile, Form, File, HTTPException, Body
from fastapi.responses import RedirectResponse, JSONResponse
from celery.result import AsyncResult
from celery import chain

from app.config import Settings, get_config
from app.utils.cred import check_auth_all
from app.tasks import task_convert_to_audio, task_upload_to_youtube
from app.models import Snippet, TaskSubmitted, TaskStatus, LocalUploadData


logger = logging.getLogger(__name__)


core = APIRouter()


@core.get("/test")
async def test():
    try:
        user_info = check_auth_all()
    except Exception as ex:
        logger.exception(ex)
        return RedirectResponse("/authorize")
    else:
        return user_info


@core.get("/task/{task_id}", response_model=TaskStatus)
async def get_task_status(task_id: str) -> dict:
    """
    Return the status of the submitted Task
    """
    task_result = AsyncResult(task_id)
    result = task_result.result

    if task_result.failed():
        result = {
            "error": str(task_result.result),
            "traceback": task_result.traceback,
        }
    return {
        "id": task_id,
        "status": task_result.status,
        "result": result,
    }


def save_upload_file_tmp(upload_file: UploadFile, config: Settings) -> Path:
    try:
        suffix = Path(upload_file.filename).suffix
        with NamedTemporaryFile(
            delete=False, suffix=suffix, dir=config.media_base
        ) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = Path(tmp.name)
    finally:
        upload_file.file.close()
    return tmp_path


@core.post("/convert-and-upload-to-youtube", response_model=TaskSubmitted)
async def convert_and_upload(
    audio: UploadFile = File(description="A audio file"),
    snippet: Snippet = Depends(),
    email: str = Form(...),
    image: UploadFile = None,
    config: Settings = Depends(get_config),
):
    src_audio_path = str(save_upload_file_tmp(audio, config))
    src_image = (
        str(save_upload_file_tmp(image, config)) if image else config.default_a2v_image
    )
    chained_task = chain(
        task_convert_to_audio.s(src_audio_path, src_image),
        task_upload_to_youtube.s(email, **snippet.dict()),
    )
    task = chained_task.apply_async()
    return JSONResponse({"task_id": task.id})


@core.post("/upload-to-youtube", response_model=TaskSubmitted)
async def upload_to_youtube(
    video: UploadFile,
    email: str = Form(...),
    snippet: Snippet = Depends(),
    config: Settings = Depends(get_config),
):
    src_video = str(save_upload_file_tmp(video, config))
    task = task_upload_to_youtube.apply_async(
        args=[src_video, email], kwargs=snippet.dict()
    )
    return {"task_id": task.id}


@core.post(
    "/upload-local-to-youtube",
    response_model=TaskSubmitted,
)
async def upload_local_to_youtube(data: LocalUploadData = Body(...), config: Settings = Depends(get_config),):
    path = data.local_file
    if not path.match(config.external_pattern) or not path.is_file():
        raise HTTPException(status_code=400, detail="invalid local file")
    task = task_upload_to_youtube.apply_async(
        args=[str(data.local_file), data.email], kwargs=data.snippet.dict()
    )
    return {"task_id": task.id}
