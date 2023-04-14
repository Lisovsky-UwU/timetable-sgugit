import functools
from datetime import date
from telebot import types
from telebot import TeleBot
from loguru import logger

from . import MessageHandler
from . import CallbackHandler
from . import markups
from . import helpers
from . import templates
from ..factory import ControllerFactory


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


def group_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|')
    message = None
    markup = None
    if len(data) == 1: # 'group'
        message = templates.MESSAGE_SELECT_INSTITUTE
        markup  = markups.institute()

    if len(data) == 2: # 'group|<I>'
        message = templates.MESSAGE_SELECT_FORM
        markup = markups.education_forms(data)

    if len(data) == 3: # 'group|<I>|<F>'
        message = templates.MESSAGE_SELECT_COURSE
        markup = markups.course(data)

    if len(data) == 4: # 'group|<I>|<F>|<C>
        message = templates.MESSAGE_SELECT_GROUP
        markup = markups.group_list(data)

    if len(data) == 5: # 'group|<I>|<F>|<C>|<G>|
        data.extend(date.today().strftime('%m.%Y|%d').split('|'))

    if len(data) == 6: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>
        data.append('1')

    if len(data) == 7: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>|<D>
        message = helpers.build_lesson_group_list(data)
        markup = markups.lesson_list(data)
    
    if len(data) == 8: # 'group|<I>|<F>|<C>|<G>|<M>.<Y>|<D>|calendar
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

    if data[2] == 'search': # 'teacher|<`P>|search...'

        if len(data) == 3: # 'teacher|<P>|search'
            msg = bot.edit_message_text(
                templates.MESSAGE_SEARCH_TEACHER, 
                callback.message.chat.id, 
                callback.message.id, 
                reply_markup = markups.cancle(data)
            )
            bot.register_next_step_handler(msg, helpers.search_teacher, menu_message_id=callback.message.id, bot=bot, data=data)
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

    if len(data) == 3: # 'teacher|<P>|<T>'
        data.extend(date.today().strftime('%m.%Y|%d').split('|'))

    if len(data) == 4: # 'teacher|<P>|<T>|<M>.<Y>'
        data.append('1')

    if len(data) == 5: # 'teacher|<P>|<T>|<M>.<Y>|<D>'
        message = helpers.build_lesson_teacher_list(data)
        markup = markups.lesson_list(data)

    if len(data) == 6: # 'teacher|<P>|<T>|<M>.<Y>|<D>|calendar'
        message = templates.MESSAGE_SELECT_DAY
        markup = markups.calendar_markup(data)

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def audience_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|')
    message = None
    markup = None

    if len(data) == 1: # 'audience'
        message = templates.MESSAGE_SELECT_BUILDING
        markup = markups.buildings(data)
    
    if len(data) == 2: # 'audience|<B>'
        message = templates.MESSAGE_SELECT_AUDIENCE
        markup = markups.audience_list(data)

    if len(data) == 3: # 'audience|<B>|<A>'
        data.extend(date.today().strftime('%m.%Y|%d').split('|'))

    if len(data) == 4: # 'audience|<B>|<A>|<M>.<Y>'
        data.append('01')
    
    if len(data) == 5: # 'audience|<B>|<A>|<M>.<Y>|<D>'
        message = helpers.build_lesson_audience_list(data)
        markup = markups.lesson_list(data)

    if len(data) == 6: # 'audience|<B>|<A>|<M>.<Y>|<D>|calendar'
        message = templates.MESSAGE_SELECT_DAY
        markup = markups.calendar_markup(data)

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def favorite_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def feedback_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def empty_callback(callback: types.CallbackQuery, bot: TeleBot):
    pass
