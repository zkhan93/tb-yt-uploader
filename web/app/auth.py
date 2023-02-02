import logging
import os

import secrets
from fastapi import APIRouter, Request, Depends, Security, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

import google_auth_oauthlib.flow
import googleapiclient.discovery


from app.config import Settings, get_config
from app.config import get_config
from app.utils.cred import SCOPES, save_cred

logger = logging.getLogger(__name__)

API_KEY_NAME = "access_token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


def check_api_key(
    config: Settings = Depends(get_config), api_key: str = Security(api_key_header)
):
    if not secrets.compare_digest(api_key.encode(), config.access_token.encode()):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


auth = APIRouter()


@auth.get("/authorize")
async def authorize(request: Request, config: Settings = Depends(get_config)):
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        config.client_secret_json, scopes=SCOPES
    )
    flow.redirect_uri = config.oauth_redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    request.session["state"] = state
    return RedirectResponse(authorization_url)


@auth.get("/thankyou")
async def thanks():
    return JSONResponse(
        dict(
            message=f"You have successfully authorized the app! proceed to make calls to the api calls"
        )
    )


@auth.get("/oauth-callback")
async def oauth_callback(request: Request, config: Settings = Depends(get_config)):
    state = request.session["state"]
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        config.client_secret_json, scopes=SCOPES, state=state
    )
    flow.redirect_uri = config.oauth_redirect_uri
    authorization_response = str(request.url)
    if os.getenv("OAUTHLIB_INSECURE_TRANSPORT", None) != "1":
        logger.info(authorization_response)
        authorization_response = authorization_response.replace("http:", "https:")
        logger.info(authorization_response)
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()
    email = user_info["email"]
    save_cred(email, credentials)
    return RedirectResponse(f"/thankyou")
