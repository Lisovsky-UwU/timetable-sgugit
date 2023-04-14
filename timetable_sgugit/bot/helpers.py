from typing import List
from telebot import types
from telebot import TeleBot
from datetime import datetime

from . import markups
from . import templates
from ..utils import get_week_number
from ..utils import format_audience_str
from ..factory import ControllerFactory
from ..constants import HOURS_TYPE
from ..constants import LESSON_TYPE
from ..constants import WEEKDAYS_TEXT


def build_lesson_group_list(data: List[str]) -> str:
    month = f'{data[5][:2]}.{data[5][-2:]}'
    group_id = int(data[4])
    lesson_list = ControllerFactory.lesson().get(
        group = group_id, date = f'{data[6]}.{month}'
    )
    group = ControllerFactory.group().get_by_id(group_id)
    
    list_lesson_str = '\n'.join(
        templates.LESSON_GROUP_INFO.format(
            lesson.hour + 1,
            HOURS_TYPE[lesson.hour],
            lesson.lesson_name,
            lesson.teacher,
            LESSON_TYPE[lesson.lesson_type],
            format_audience_str(lesson.audience),
        )
        for lesson in lesson_list
    )

    _select_day = datetime.strptime(f'{data[6]}.{data[5]}', '%d.%m.%Y').date()
    return templates.MESSAGE_GROUP_LESSON_LIST.format(
        group.name,
        f'{data[6]}.{data[5]} - {WEEKDAYS_TEXT[_select_day.weekday()]}',
        get_week_number(_select_day),
        list_lesson_str if len(lesson_list) != 0 else templates.NO_LESSON_ON_DAY
    )


def build_lesson_teacher_list(data: List[str]) -> str:
    month = f'{data[-2][:2]}.{data[-2][-2:]}'
    teacher_id = int(data[-3])
    lesson_list = ControllerFactory.lesson().get(
        teacher = teacher_id, date = f'{data[-1]}.{month}'
    )
    teacher = ControllerFactory.teacher().get_by_id(teacher_id)

    list_lesson_str = '\n'.join(
        templates.LESSON_TEACHER_INFO.format(
            lesson.hour + 1,
            HOURS_TYPE[lesson.hour],
            lesson.lesson_name,
            lesson.group,
            LESSON_TYPE[lesson.lesson_type],
            format_audience_str(lesson.audience),
        )
        for lesson in lesson_list
    )

    _select_day = datetime.strptime(f'{data[-1]}.{data[-2]}', '%d.%m.%Y').date()
    return templates.MESSAGE_TEACHER_LESSON_LIST.format(
        teacher.name,
        f'{data[-1]}.{data[-2]} - {WEEKDAYS_TEXT[_select_day.weekday()]}',
        get_week_number(_select_day),
        list_lesson_str if len(lesson_list) != 0 else templates.NO_LESSON_ON_DAY
    )


def search_teacher(
    message: types.Message, 
    menu_message_id: int,
    bot: TeleBot, 
    data: List[str], 
):
    data.extend([ message.text, '1' ]) # Добавляем в данные сообщение для поиска и номер страницы
    bot.delete_message(message.chat.id, menu_message_id)
    bot.send_message(
        message.chat.id,
        templates.MESSAGE_SELECT_TEACHER, 
        reply_markup=markups.teacher_list(
            data,
            ControllerFactory.teacher().search_by_name(message.text),
            False
        )
    )


def build_lesson_audience_list(data: List[str]):
    month = f'{data[-2][:2]}.{data[-2][-2:]}'
    audience_id = int(data[-3])
    lesson_list = ControllerFactory.lesson().get(
        audience = audience_id, date = f'{data[-1]}.{month}'
    )
    audience = ControllerFactory.audience().get_by_id(audience_id)

    list_lesson_str = '\n'.join(
        templates.LESSON_AUDIENCE_INFO.format(
            lesson.hour + 1,
            HOURS_TYPE[lesson.hour],
            lesson.lesson_name,
            lesson.teacher,
            lesson.group,
            LESSON_TYPE[lesson.lesson_type],
        )
        for lesson in lesson_list
    )

    _select_day = datetime.strptime(f'{data[-1]}.{data[-2]}', '%d.%m.%Y').date()
    return templates.MESSAGE_AUDIENCE_LESSON_LIST.format(
        audience.name,
        f'{data[-1]}.{data[-2]} - {WEEKDAYS_TEXT[_select_day.weekday()]}',
        get_week_number(_select_day),
        list_lesson_str if len(lesson_list) != 0 else templates.NO_LESSON_ON_DAY
    )
