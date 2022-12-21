import logging
import os

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import google_auth_oauthlib.flow
import googleapiclient.discovery

from app.config import get_config
from app.utils.cred import get_credential, SCOPES, save_cred

logger = logging.getLogger(__name__)


config = get_config()
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.secret_key)


@app.get("/test")
async def test(request: Request):
    try:
        with get_credential(config.youtube_email) as credentials:
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


@app.get("/authorize")
async def authorize(request: Request):
    config = get_config()
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        config.client_secret_json, scopes=SCOPES
    )
    flow.redirect_uri = config.oauth_redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    request.session["state"] = state
    return RedirectResponse(authorization_url)


@app.get("/oauth-callback")
async def oauth_callback(request: Request):
    state = request.session["state"]
    config = get_config()
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
