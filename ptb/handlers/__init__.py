from .commands import get_clean_handler, get_start_handler
from .convert import get_convert_handler


message_handlers = [

]

command_handlers = [get_clean_handler, get_start_handler, get_convert_handler]
all_handlers = command_handlers + message_handlers
