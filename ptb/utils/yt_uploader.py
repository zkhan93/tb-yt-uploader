import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaFileUpload
from config import get_config
from utils.cred import get_credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def upload_to_youtube(filepath, **kwargs):
    api_service_name = "youtube"
    api_version = "v3"
    config = get_config()
    with get_credentials(config.youtube_email) as credentials:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )
        snippet = kwargs.copy()
        if "title" not in snippet:
            snippet["title"] = "New Video"

        snippet.update(
            tags=["islamic"],
            categoryId="22",
        )
        body = dict(
            snippet=snippet,
            status=dict(privacyStatus="public", selfDeclaredMadeForKids=True),
        )
        request = youtube.videos().insert(
            part=",".join(body.keys()), body=body, media_body=MediaFileUpload(filepath)
        )
        response = request.execute()
    return response

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
