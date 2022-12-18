import os
from telegram.ext import CommandHandler, Filters
from app.config import Settings


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
    allowed_usernames = [ue[0] for ue in config.allowed_users]
    return CommandHandler(
        "clean", clean, filters=Filters.chat(username=allowed_usernames)
    )
