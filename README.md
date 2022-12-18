# How to RUN
- copy the docker-compose.yml file to a folder 
- create a `.env` file with following variables
    ```js
    TOKEN=`<telegram bot token from botfather>`
    ALLOWED_USERS=`<username>:<email>`
    CLIENT_SECRET_JSON=`<base 64 dump of oauth client secret file from google>`
    MEDIA_BASE=/data
    OAUTH_REDIRECT_URI=`https://<yourdomain>/oauth-callback`
    SECRET_KEY=`<randomly generated secret string should be more that 32 characters>`
    REDIS_HOST=redis
    YOUTUBE_EMAIL=`<email of account where you want to upload the video>`
    ```
- start the containers 
`docker-compose up -d`
