import logging

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


logger = logging.getLogger(__name__)


frontend = APIRouter()

@frontend.get("/")
async def index():
    return HTMLResponse(open("./html/index.html", "r").read())

@frontend.get("/privacy")
async def privacy():
    return HTMLResponse(open("./html/privacy_policy.html", "r").read())
