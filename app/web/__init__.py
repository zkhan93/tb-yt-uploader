import logging

from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import whisper

from app.config import get_config
from app.utils.cred import get_cred, save_cred

logger = logging.getLogger(__name__)


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

config = get_config()
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config.secret_key)


@app.get("/audio2text/{filename}")
async def test_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(f"./data/audios/{filename}.ogg")
    return result


@app.get("/test")
async def test(request: Request):
    email = "shaheenkaimuri@gmail.com"
    try:
        credentials = get_cred(email)
    except Exception as ex:
        logger.exception(ex)
        return RedirectResponse("/authorize")

    print(credentials)
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**credentials)
    service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()

    save_cred(email, credentials)

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
    # this is a redirect
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
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()
    email = user_info["email"]
    save_cred(email, credentials)
    return "ok"
