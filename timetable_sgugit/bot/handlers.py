import functools
from datetime import datetime
from datetime import date
from telebot import types
from telebot import TeleBot
from loguru import logger
from typing import List

from . import Handler
from . import MessageHandler
from . import CallbackHandler
from . import markups
from . import templates
from ..factory import ControllerFactory
from ..constants import HOURS_TYPE
from ..constants import LESSON_TYPE
from ..constants import WEEKDAYS_TEXT
from ..utils import format_audience_str
from ..utils import get_week_number


def message_handle_exceptions(handler: MessageHandler):
    @functools.wraps(handler)
    def decorator(message: types.Message, bot: TeleBot):
        logger.debug(f'Вызывается message обработчик {handler.__name__} пользователем @{message.from_user.username} (data: "{message.text}")')
        try:
            return handler(message, bot)
        except Exception as e:
            logger.error(f'В чате с @{message.from_user.username} (message: {message.text}) возникла ошибка: {e}')
    
    return decorator


def callback_handle_exceptions(handler: CallbackHandler):
    @functools.wraps(handler)
    def decorator(arg: types.CallbackQuery, bot: TeleBot):
        logger.debug(f'Вызывается callback обработчик {handler.__name__} пользователем @{arg.from_user.username} (data: "{arg.data}")')
        try:
            return handler(arg, bot)
        except Exception as e:
            logger.error(f'В чате с @{arg.from_user.username} (message: {arg.data}) возникла ошибка: {e}')
    
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


def _build_lesson_group_list(data: List[str]) -> str:
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


def _build_lesson_teacher_list(data: List[str]) -> str:
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


def _search_teacher(
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


def group_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|')
    message = None
    markup = None
    if len(data) == 1: # 'group'
        message = templates.MESSAGE_SELECT_INSTITUTE
        markup  = markups.institute()

    elif len(data) == 2: # 'group|<I>'
        message = templates.MESSAGE_SELECT_FORM
        markup = markups.education_forms(data)

    elif len(data) == 3: # 'group|<I>|<F>'
        message = templates.MESSAGE_SELECT_COURSE
        markup = markups.course(data)

    elif len(data) == 4: # 'group|<I>|<F>|<C>
        message = templates.MESSAGE_SELECT_GROUP
        markup = markups.group_list(data)

    elif len(data) == 5: # 'group|<I>|<F>|<C>|<G>|
        data.extend(date.today().strftime('%m.%Y|%d').split('|'))
        message = _build_lesson_group_list(data)
        markup = markups.lesson_list(data)

    elif len(data) == 6: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>
        data.append('1')
        message = _build_lesson_group_list(data)
        markup = markups.lesson_list(data)

    elif len(data) == 7: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>|<D>
        message = _build_lesson_group_list(data)
        markup = markups.lesson_list(data)
    
    elif len(data) == 8: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>|<D>|calendar
        message = templates.MESSAGE_SELECT_DAY
        markup = markups.calendar_markup(data)


    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def teacher_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|')
    message = None
    markup = None

    if len(data) == 1:
            data.append('1')

    if len(data) == 2: # 'teacher|<P>'
        message = templates.MESSAGE_SELECT_TEACHER
        markup = markups.teacher_list(data)

    elif data[2] == 'search': # 'teacher|<`P>|search...'

        if len(data) == 3: # 'teacher|<P>|search'
            msg = bot.edit_message_text(
                templates.MESSAGE_SEARCH_TEACHER, 
                callback.message.chat.id, 
                callback.message.id, 
                reply_markup = markups.cancle(data)
            )
            bot.register_next_step_handler(msg, _search_teacher, menu_message_id=callback.message.id, bot=bot, data=data)
            return
        
        elif len(data) == 4 and data[-1] == 'cancle': # 'teacher|<P>|search|cancle'
            bot.clear_step_handler_by_chat_id(callback.message.chat.id)
            data = data[:2]
            message = templates.MESSAGE_SELECT_TEACHER
            markup = markups.teacher_list(data)
        
        elif len(data) == 4: # 'teacher|<P>|search|<S>'
            data.append('1')
            message = templates.MESSAGE_SELECT_TEACHER
            markup = markups.teacher_list(data, ControllerFactory.teacher().search_by_name(data[3]), False)
        
        elif len(data) == 5: # 'teacher|<P>|search|<S>|<P2>'
            message = templates.MESSAGE_SELECT_TEACHER
            markup = markups.teacher_list(data, ControllerFactory.teacher().search_by_name(data[3]), False)

    elif len(data) == 3: # 'teacher|<P>|<T>'
        data.extend(date.today().strftime('%m.%Y|%d').split('|'))
        message = _build_lesson_teacher_list(data)
        markup = markups.lesson_list(data)

    elif len(data) == 4: # 'teacher|<P>|<T>|<M>.<Y>'
        data.append('1')
        message = _build_lesson_teacher_list(data)
        markup = markups.lesson_list(data)

    elif len(data) == 5: # 'teacher|<P>|<T>|<M>.<Y>|<D>'
        message = _build_lesson_teacher_list(data)
        markup = markups.lesson_list(data)

    elif len(data) == 6: # 'teacher|<P>|<T>|<M>.<Y>|<D>|calendar'
        message = templates.MESSAGE_SELECT_DAY
        markup = markups.calendar_markup(data)


    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def audience_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def favorite_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def feedback_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def empty_callback(callback: types.CallbackQuery, bot: TeleBot):
    pass
