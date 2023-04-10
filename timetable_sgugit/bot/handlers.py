import functools
from telebot import types
from telebot import TeleBot
from loguru import logger
from typing import Union

from . import Handler
from . import markups
from . import templates


def handle_exceptions(handler: Handler):
    @functools.wraps(handler)
    def decorator(arg: Union[types.Message, types.CallbackQuery], bot: TeleBot):
        message = arg.message if isinstance(arg, types.CallbackQuery) else arg
        logger.debug(f'Вызывается обработчик {handler.__name__} пользователем @{message.from_user.username} (message: "{message.text}")')
        try:
            return handler(arg, bot)
        except Exception as e:
            error_message = f'Возникла ошибка: {e}'
            logger.error(f'В чате с @{message.from_user.username} (message: {message.text}) возникла ошибка: {e}')
            bot.send_message(message.chat.id, error_message)
    
    return decorator


def start(message: types.Message, bot: TeleBot):
    bot.send_message(message.chat.id, templates.MESSAGE_MAIN_MENU, reply_markup=markups.main_menu_markup())


def main_menu_callback(callback: types.CallbackQuery, bot: TeleBot):
    bot.edit_message_text(
        templates.MESSAGE_MAIN_MENU,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = markups.main_menu_markup()
    )


def group_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def teacher_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def audience_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def favorite_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def feedback_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...
