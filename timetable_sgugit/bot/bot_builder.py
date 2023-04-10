from typing import Dict
from typing import Any
from telebot import TeleBot
from telebot import types

from . import MessageHandler
from . import CallbackHandler
from .handlers import handle_exceptions
from .handlers import start
from .handlers import group_callback
from .handlers import teacher_callback
from .handlers import audience_callback
from .handlers import favorite_callback
from .handlers import feedback_callback
from .handlers import main_menu_callback
from ..constants import BOT_TOKEN


message_handlers: Dict[MessageHandler, Any] = {
    start : { 'commands': ['start'] },
}

callback_handlers: Dict[CallbackHandler, Any] = {
    group_callback     : { 'func': lambda call: call.data.startswith('group') },
    teacher_callback   : { 'func': lambda call: call.data.startswith('teahcer') },
    audience_callback  : { 'func': lambda call: call.data.startswith('audience') },
    favorite_callback  : { 'func': lambda call: call.data.startswith('favorite') },
    feedback_callback  : { 'func': lambda call: call.data.startswith('feedback') },
    main_menu_callback : { 'func': lambda call: call.data.startswith('main_menu') },
}

command_list = {
    '/start' : 'Запустить бота',
}


def build_bot() -> TeleBot:
    bot = TeleBot(BOT_TOKEN)

    for handler, filter in message_handlers.items():
        decorated = handle_exceptions(handler)
        bot.register_message_handler(decorated, pass_bot=True, **filter)

    for handler, filter in callback_handlers.items():
        decorated = handle_exceptions(handler)
        bot.register_callback_query_handler(decorated, pass_bot=True, **filter)

    bot.set_my_commands( [ types.BotCommand(cmd, dscr) for cmd, dscr in command_list.items() ] )

    return bot
