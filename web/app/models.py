from pydantic import BaseModel as PydanticBase, Extra

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
