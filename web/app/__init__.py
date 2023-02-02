import logging

from fastapi import FastAPI, Depends
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.auth import check_api_key
from app.config import Settings

logger = logging.getLogger(__name__)


def create_app(config: Settings) -> FastAPI:
    from .auth import auth as auth_app
    from .core import core as core_app

    app = FastAPI(title="Youtube Helper",description="a description")
    app.add_middleware(SessionMiddleware, secret_key=config.secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        auth_app,
        tags=["Authentication"],
        prefix="",
    )
    app.include_router(
        core_app,
        dependencies=[Depends(check_api_key)],
        tags=["Core"],
        prefix="",
    )

    return app
