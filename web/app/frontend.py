import logging

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse


logger = logging.getLogger(__name__)


frontend = APIRouter()

@frontend.get("/")
async def index():
    return HTMLResponse(open("./html/index.html", "r").read())

@frontend.get("/privacy")
async def privacy():
    return HTMLResponse(open("./html/privacy_policy.html", "r").read())

@frontend.get("/terms-of-service")
async def terms():
    return HTMLResponse(open("./html/tos.html", "r").read())

@frontend.get("/favicon.ico", response_class=FileResponse)
async def favicon():
    return FileResponse("./html/favicon.ico")

@frontend.get("/icon-512.png", response_class=FileResponse)
async def icon_512():
    return FileResponse("./html/icon-512.png")
