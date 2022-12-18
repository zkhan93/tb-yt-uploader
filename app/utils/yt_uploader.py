import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials
from app.config import get_config
from app.utils.cred import get_cred, save_cred

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def upload_to_youtube(filepath, description):
    api_service_name = "youtube"
    api_version = "v3"
    config = get_config()
    email = "shaheenkaimuri@gmail.com"
    credentials = get_cred(email)
    print(credentials)
    credentials = google.oauth2.credentials.Credentials(**credentials)
    service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()
    print(user_info)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
    body = dict(
        snippet=dict(
            title="First video from ptb",
            description=description,
            tags=["islamic"],
            categoryId="22",
        ),
        status=dict(privacyStatus="public", selfDeclaredMadeForKids=True),
    )
    request = youtube.videos().insert(
        part=",".join(body.keys()), body=body, media_body=MediaFileUpload(filepath)
    )
    response = request.execute()
    save_cred(email, credentials)
    print(response)

    # response = None
    # def upload_next_chunk(request):
    #     status, response = request.next_chunk()
    #     if status:
    #         print("Uploaded %d%%." % int(status.progress() * 100))
    #     return response

    # retry_limit = 5
    # fail_count = 1
    # while response is None:
    #     try:
    #         upload_next_chunk()
    #     except googleapiclient.errors.HttpError as e:
    #         if e.resp.status in [404]:
    #             pass# Start the upload all over again.
    #         elif e.resp.status in [500, 502, 503, 504]:
    #             pass # Call next_chunk() again, but use an exponential backoff for repeated errors.
    #             upload_next_chunk()
    #         else:
    #             pass # Do not retry. Log the error and fail.
    #     else:
    #         print("Upload Complete!")
