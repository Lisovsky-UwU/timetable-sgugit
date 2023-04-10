from typing import Callable
from typing import Union
from telebot import types
from telebot import TeleBot


MessageHandler = Callable[[types.Message, TeleBot], None]
CallbackHandler = Callable[[types.CallbackQuery, TeleBot], None]
Handler = Union[MessageHandler, CallbackHandler]

from .bot_builder import build_bot
