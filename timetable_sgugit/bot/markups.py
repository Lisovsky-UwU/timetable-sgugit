from math import ceil
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
    '''Последние аргументы должны быть следующими: [ "<M>.<Y>", "<D>", "<SOME_STR>" ] '''
    month = int(cur_data[-3].split('.')[0])
    year = int(cur_data[-3].split('.')[1])

    cur_data_str = '|'.join(cur_data[:-3])

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

    _prev_date_str = cur_data.copy()
    _prev_date_str[-3] = get_prev_month(month, year)
    _next_date_str = cur_data.copy()
    _next_date_str[-3] = get_next_month(month, year)
    # _prev_data_str = '|'.join(cur_data[:-3])
    keyboard.row(
        InlineKeyboardButton(templates.BTN_PREV_MONTH, callback_data='|'.join(_prev_date_str)),
        InlineKeyboardButton(templates.BTN_NEXT_MONTH, callback_data='|'.join(_next_date_str)),
    )
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-1])))
    return keyboard


def lesson_list(cur_data: List[str]):
    cur_data_str = '|'.join(cur_data)
    keyboard = InlineKeyboardMarkup()

    _date = datetime.strptime(f'{cur_data[-1]}.{cur_data[-2]}', '%d.%m.%Y').date()
    _next_day = _date + timedelta(days=1)
    _prev_day = _date - timedelta(days=1)

    _day_switch_data = '|'.join(cur_data[:-2])
    keyboard.row(
        InlineKeyboardButton(templates.BTN_PREV_DAY, callback_data=f'{_day_switch_data}|{_prev_day.strftime("%m.%Y|%d")}'),
        InlineKeyboardButton(templates.BTN_NEXT_DAY, callback_data=f'{_day_switch_data}|{_next_day.strftime("%m.%Y|%d")}'),
    )

    keyboard.add(InlineKeyboardButton(templates.BTN_OPEN_CALENDAR, callback_data=f'{cur_data_str}|calendar'))
    keyboard.add(InlineKeyboardButton(templates.BTN_MAIN_MENU, callback_data=f'main_menu'))
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='|'.join(cur_data[:-3])))
    return keyboard


def teacher_list(cur_data: List[str]):
    '''Последним элементом обязательно должен быть номер страницы'''
    page = int(cur_data[-1])
    _teacher_list = ControllerFactory.teacher().get_all()
    _page_size = 10
    _page_count = ceil(len(_teacher_list) / float(_page_size))

    keyboard = InlineKeyboardMarkup()

    for index in range((page - 1) * _page_size, (page - 1) * _page_size + _page_size):
        if index >= len(_teacher_list):
            break
        keyboard.add(InlineKeyboardButton(_teacher_list[index].name, callback_data=f'teacher|{page}|{_teacher_list[index].id}'))

    data_str_page = '|'.join(cur_data[:-1])
    keyboard.row(
        InlineKeyboardButton(templates.BTN_PREV_PAGE, callback_data=f'{data_str_page}|{page - 1 if page > 1 else 1}'),
        InlineKeyboardButton(f'{page} из {_page_count}', callback_data=f'{data_str_page}|{page}'),
        InlineKeyboardButton(templates.BTN_NEXT_PAGE, callback_data=f'{data_str_page}|{page + 1 if page < _page_count else page}')
    )
    keyboard.add(InlineKeyboardButton(templates.BTN_BACK, callback_data='main_menu'))
    return keyboard
