import googleapiclient.discovery
import googleapiclient.errors
from pathlib import Path
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from app.utils.cred import get_credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]


def upload_to_youtube(video_file, email, delete=False, **kwargs):
    api_service_name = "youtube"
    api_version = "v3"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cameraLocation="Village Location",
    with get_credentials(email) as credentials:
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials
        )
            
        snippet = kwargs.copy()
        if "title" not in snippet:
            snippet["title"] = f"{cameraLocation} CCTV Feed - {current_time}"
        if "description" not in snippet:
            snippet["description"] = f"Live CCTV footage from {cameraLocation} captured on {current_time}. Watch and stay updated with real-time events in the village."
        if "tags" not in snippet:
            snippet["tags"] = ["village", "CCTV", "live feed", "security", "real-time", "monitoring"],
        if "categoryId" not in snippet:
            snippet["categoryId"] = "22"
        
        body = dict(
            snippet=snippet,
            status=dict(privacyStatus="private", selfDeclaredMadeForKids=False),
        )
        request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file),
        )
        response = request.execute()

    if response.get("status", {}).get("uploadStatus", "failed") == "uploaded" and delete:
        Path(video_file).unlink()
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
