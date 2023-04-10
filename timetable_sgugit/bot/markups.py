from typing import List
from datetime import date
from datetime import datetime
from datetime import timedelta
from calendar import Calendar
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from . import templates
from ..factory import ControllerFactory
from ..constants import COURSES
from ..constants import INSTITUTS
from ..constants import MONTHS_LIST
from ..constants import WEEKDAY_LIST
from ..constants import EDUCATION_FORMS
from ..utils import get_next_month
from ..utils import get_prev_month


def main_menu_markup():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_GROUP, callback_data='group'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_TEACHER, callback_data='teacher'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_AUDIENCE, callback_data='audience'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_FAVORITE, callback_data='favorite'))
    keyboard.add(InlineKeyboardButton(templates.BTN_SELECT_FEEDBACK, callback_data='feedback'))

    return keyboard


def institute(back_data: str = 'main_menu'):
    keyboard = InlineKeyboardMarkup()
    for inst_k, inst_v in INSTITUTS.items():
        keyboard.add(InlineKeyboardButton(inst_v, callback_data=f'group|{inst_k}'))

    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data=back_data))
    return keyboard


def education_forms(cur_data: List[str]):
    cur_data_str = '|'.join(cur_data)
    keyboard = InlineKeyboardMarkup()
    for form_k, form_v in EDUCATION_FORMS.items():
        keyboard.add(InlineKeyboardButton(form_k, callback_data=f'{cur_data_str}|{form_v}'))

    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-1])))
    return keyboard


def course(cur_data: List[str]):
    institute = int(cur_data[1])

    cur_data_str = '|'.join(cur_data)
    keyboard = InlineKeyboardMarkup()
    for course in COURSES[institute]:
        keyboard.add(InlineKeyboardButton(course, callback_data=f'{cur_data_str}|{course}'))

    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-1])))
    return keyboard


def group_list(cur_data: List[str]):
    _group_list = ControllerFactory.group().get(
        int(cur_data[1]),
        int(cur_data[2]),
        int(cur_data[3])
    )

    cur_data_str = '|'.join(cur_data)
    keyboard = InlineKeyboardMarkup()
    keys_row = list()
    for index, group in enumerate(_group_list, 1):
        keys_row.append(InlineKeyboardButton(group.name, callback_data=f'{cur_data_str}|{group.id}'))
        if index % 3 == 0:
            keyboard.row(*keys_row)
            keys_row.clear()

    keyboard.row(*keys_row)
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-1])))
    return keyboard



def calendar_markup(cur_data: List[str]):
    '''Последний аргумент должен быть месяцем и годом в формате ДД.ММ'''
    month = int(cur_data[-1].split('.')[0])
    year = int(cur_data[-1].split('.')[1])

    cur_data_str = '|'.join(cur_data[:-1])

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f'{MONTHS_LIST[month - 1]} - {year} г.', callback_data=f'empty'))
    keyboard.row(
        *[
            InlineKeyboardButton(f'{_week_day}', callback_data=f'empty')
            for _week_day in WEEKDAY_LIST
        ]
    )
    for week in Calendar().monthdatescalendar(year, month):
        keyboard.row(
            *[
                InlineKeyboardButton(day.day, callback_data=f'{cur_data_str}|{day.strftime("%m.%Y")}|{day.day}')
                for day in week
            ]
        )

    _prev_data_str = '|'.join(cur_data[:-1])
    keyboard.row(
        InlineKeyboardButton(templates.BTN_PREV_MONTH, callback_data=f'{_prev_data_str}|{get_prev_month(month, year)}'),
        InlineKeyboardButton(templates.BTN_NEXT_MONTH, callback_data=f'{_prev_data_str}|{get_next_month(month, year)}')
    )
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data=_prev_data_str))
    return keyboard


def lesson_list(cur_data: List[str]):
    # cur_data_str = '|'.join(cur_data[:-1])
    keyboard = InlineKeyboardMarkup()

    _date = datetime.strptime(f'{cur_data[-1]}.{cur_data[-2]}', '%d.%m.%Y').date()
    _next_day = _date + timedelta(days=1)
    _prev_day = _date - timedelta(days=1)

    _day_switch_data = '|'.join(cur_data[:-2])
    keyboard.row(
        InlineKeyboardButton(templates.BTN_PREV_DAY, callback_data=f'{_day_switch_data}|{_prev_day.strftime("%m.%Y|%d")}'),
        InlineKeyboardButton(templates.BTN_NEXT_DAY, callback_data=f'{_day_switch_data}|{_next_day.strftime("%m.%Y|%d")}'),
    )

    keyboard.add(InlineKeyboardButton(templates.BTN_OPEN_CALENDAR, callback_data='|'.join(cur_data[:-1])))
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-3])))
    return keyboard
