import os
import logging
from telegram.ext import Updater
from config import get_config, Settings
from handlers import all_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger("bot")


def register_handlers(config: Settings, dispatcher):
    for h in all_handlers:
        try:
            dispatcher.add_handler(h(config))
        except Exception as ex:
            logger.exception(f"fail to register handler {h.__name__}")


def env_setup(config: Settings):
    # make sure media folder exists
    IMAGES_DIR = os.path.join(config.media_base, "images")
    AUDIOS_DIR = os.path.join(config.media_base, "audios")
    VIDEOS_DIR = os.path.join(config.media_base, "videos")
    for dir in [IMAGES_DIR, AUDIOS_DIR, VIDEOS_DIR]:
        if not os.path.exists(dir):
            os.mkdir(dir)


def run():
    config: Settings = get_config()
    # env_setup(config)
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher
    register_handlers(config, dispatcher)
    updater.start_polling()


if __name__ == "__main__":
    run()
