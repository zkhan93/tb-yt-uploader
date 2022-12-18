from app.handlers.audio2video import get_handler as get_audio2video_handler
from app.handlers.commands import get_clean_handler, get_start_handler


message_handlers = [
    get_audio2video_handler,
]
command_handlers = [get_clean_handler, get_start_handler]
all_handlers = command_handlers + message_handlers
