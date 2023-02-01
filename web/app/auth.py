import logging
import os

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from app.config import Settings, get_config
import google_auth_oauthlib.flow
import googleapiclient.discovery

from app.config import get_config
from app.utils.cred import get_credentials, SCOPES, save_cred

logger = logging.getLogger(__name__)


auth = APIRouter()

@auth.get("/test")
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
    return "ok"
