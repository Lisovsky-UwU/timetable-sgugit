from typing import Dict, Any

from telebot import TeleBot, types

from . import MessageHandler, CallbackHandler
from .handlers import (
    start,
    empty_callback,
    group_callback,
    regular_message,
    teacher_callback,
    audience_callback,
    favorite_callback,
    feedback_callback,
    main_menu_callback,
    message_handle_exceptions,
    callback_handle_exceptions
)
from ..configmodule import config


message_handlers: Dict[MessageHandler, Any] = {
    start           : { 'commands': ['start'] },
    regular_message : { 'func': lambda m: True },
}

callback_handlers: Dict[CallbackHandler, Any] = {
    empty_callback     : { 'func': lambda call: call.data.startswith('empty') },
    group_callback     : { 'func': lambda call: call.data.startswith('group') },
    teacher_callback   : { 'func': lambda call: call.data.startswith('teacher') },
    audience_callback  : { 'func': lambda call: call.data.startswith('audience') },
    favorite_callback  : { 'func': lambda call: call.data.startswith('favorite') },
    feedback_callback  : { 'func': lambda call: call.data.startswith('feedback') },
    main_menu_callback : { 'func': lambda call: call.data.startswith('main_menu') },
}

command_list = {
    '/start' : 'Запустить бота',
}


def build_bot() -> TeleBot:
    bot = TeleBot(config.bot.token)

    for handler, filter in message_handlers.items():
        decorated = message_handle_exceptions(handler)
        bot.register_message_handler(decorated, pass_bot=True, **filter)

    for handler, filter in callback_handlers.items():
        decorated = callback_handle_exceptions(handler)
        bot.register_callback_query_handler(decorated, pass_bot=True, **filter)

    bot.set_my_commands( [ types.BotCommand(cmd, dscr) for cmd, dscr in command_list.items() ] )

    return bot
