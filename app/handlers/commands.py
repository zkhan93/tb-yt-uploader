import os
import logging

from telegram.ext import CommandHandler, Filters

from app.config import Settings

logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm Kiyamu, I'm here to help you! see available commands",
    )


def clean(update, context):
    if os.path.exists("data"):
        os.system("rm -f ./data/*")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Cleaning up old downloaded files from data folder",
    )


def get_start_handler(config):
    return CommandHandler("start", start)


def get_clean_handler(config: Settings):
    return CommandHandler(
        "clean",
        clean,
        filters=Filters.chat(
            username=[username for username, _ in config.allowed_users]
        ),
    )
