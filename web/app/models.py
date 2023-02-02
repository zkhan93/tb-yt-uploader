from pydantic import BaseModel as PydanticBase, Extra
from typing import Optional, Any
from pathlib import Path

class BaseModel(PydanticBase):
    class Config:
        extra = Extra.forbid


class Status(BaseModel):
    selfDeclaredMadeForKids: bool = False
    privacyStatus: str = "public"


class Snippet(BaseModel):
    title: str = "New Video"
    tags: list[str] = ["islamic"]
    categoryId: list[str] = ["22"]


class VideoInfo(BaseModel):
    snippet: Snippet
    status: Status


class TaskSubmitted(BaseModel):
    task_id: str


class TaskResult(BaseModel):
    error: str
    traceback: str


class TaskStatus(BaseModel):
    id: str
    status: str
    result: Optional[Any] 

class LocalUploadData(BaseModel):
    local_file: Path
    email: str
    snippet: Snippet
