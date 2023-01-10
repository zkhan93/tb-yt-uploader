# Telegram Audio to Video Bot

A Telegram bot that can convert a given audio message to a video using FFmpeg and an image. This bot is built on Docker and has background jobs to keep the Google Auth Token alive by refreshing it every hour, using Celery Beat and Celery Task to achieve this. The bot has a web interface where you sign in using Google and give the bot access to manage your YouTube videos.

## Features
- Convert audio messages to videos using FFmpeg
- Background jobs to keep the Google Auth Token alive
- Web interface to sign in using Google and give the bot access to manage your YouTube videos
- Upload videos to YouTube
- Telegram Bot that can be used to convert audio message into video

## Getting Started

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Telegram Bot Token
- Google client secret json file
- A redirect URI, this can be `http://localhost:8000/oauth2-callback` if you are running the application on your local machine

### Installation
- Clone the repository and navigate into the project directory
- Copy `.env.example` to `.env`  and fill in the appropriate secrets
- Build and start the application by running `docker-compose up --build`
- Wait for the containers to start up and the application to initialize, this may take a few minutes

### Usage
- Access the web interface by going to `http://localhost:8000/oauth2`
- Sign in with your google account
- You will be prompted to give the bot access to manage your YouTube videos
- After signing in you can use the bot by sending an audio recording to bot and then reply on that message with "/covert <title of the video>"
- Bot will create and upload the video  to youtube and reply you with the status
- To stop the application, press `CTRL+C` in the terminal or run `docker-compose down`

## Monitoring
- Celery flower dashboard is available at `http://localhost:5555`

## Contributing

If you want to contribute to the project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
