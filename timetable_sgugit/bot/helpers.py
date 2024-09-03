from typing import List
from datetime import datetime

from telebot import types, TeleBot

from . import markups, templates
from ..utils import get_week_number, format_audience_str
from ..factory import ControllerFactory
from ..constants import HOURS_TYPE, LESSON_TYPE, WEEKDAYS_TEXT
from ..configmodule import config


def build_lesson_group_list(data: List[str]) -> str:
    month = f'{data[-2][:2]}.{data[-2][-2:]}'
    group_id = int(data[-3])
    lesson_list = ControllerFactory.lesson().get(
        group = group_id, date = f'{data[-1]}.{month}'
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

    _select_day = datetime.strptime(f'{data[-1]}.{data[-2]}', '%d.%m.%Y').date()
    return templates.MSG_GROUP_LESSON_LIST.format(
        group.name,
        f'{data[-1]}.{data[-2]} - {WEEKDAYS_TEXT[_select_day.weekday()]}',
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
    return templates.MSG_TEACHER_LESSON_LIST.format(
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
    try:
        bot.delete_message(message.chat.id, menu_message_id)
    except:
        pass
    bot.send_message(
        message.chat.id,
        templates.MSG_SELECT_TEACHER, 
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
    return templates.MSG_AUDIENCE_LESSON_LIST.format(
        audience.name,
        f'{data[-1]}.{data[-2]} - {WEEKDAYS_TEXT[_select_day.weekday()]}',
        get_week_number(_select_day),
        list_lesson_str if len(lesson_list) != 0 else templates.NO_LESSON_ON_DAY
    )


def send_feedback(
    message: types.Message,
    menu_message_id: int,
    bot: TeleBot,
):
    try:
        bot.delete_message(message.chat.id, menu_message_id)
    except:
        pass
    bot.send_message(
        message.chat.id,
        templates.MSG_FEEDBACK_IS_SEND, 
        reply_markup=markups.feedback_is_send()
    )

    feedback_controller = ControllerFactory.feedback()
    user_controller = ControllerFactory.user()

    feedback_db = feedback_controller.take_feedback(
        user_controller.get(message.chat.id).id,
        message.id
    )

    for send_to_chat_id in config.bot.feedback_send_to.split('|'):
        bot.send_message(
            send_to_chat_id,
            templates.MSG_FEEDBACK_SEND_TO.format(
                message.from_user.username
            )
        )
        send_to_message = bot.forward_message(send_to_chat_id, message.chat.id, message.id)
        feedback_controller.send_feedback_to(
            user_controller.get(send_to_chat_id).id,
            send_to_message.id,
            feedback_db.id
        )
