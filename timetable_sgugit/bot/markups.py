from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from . import templates


def main_menu_markup():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_GROUP, callback_data='group|institute'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_TEACHER, callback_data='teacher|list'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_AUDIENCE, callback_data='audience|list'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_FAVORITE, callback_data='favorite|list'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_FEEDBACK, callback_data='feedback'))

    return keyboard
