import functools
from datetime import date
from telebot import types
from telebot import TeleBot
from loguru import logger
from typing import Tuple
from typing import List

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
    ControllerFactory.user().create_if_not_exists(message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, templates.MSG_MAIN_MENU, reply_markup=markups.main_menu_markup())


def main_menu_callback(callback: types.CallbackQuery, bot: TeleBot):
    bot.edit_message_text(
        templates.MSG_MAIN_MENU,
        callback.message.chat.id,
        callback.message.id,
        reply_markup = markups.main_menu_markup()
    )


def group_interface(
    callback: types.CallbackQuery, 
    data: List[str], 
    interface_data: List[str]
) -> Tuple[str, types.ReplyKeyboardMarkup]:
    if len(interface_data) == 1:
        _tmp = date.today().strftime('%m.%Y|%d').split('|')
        data.extend(_tmp)
        interface_data.extend(_tmp)

    if len(interface_data) == 2: # '<G>|<M>.<Y>
        data.append('1')
        interface_data.append('1')

    lesson_type = f'G:{interface_data[0]}'

    if len(interface_data) == 3: # <G>|<M>.<Y>|<D>
        return helpers.build_lesson_group_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)

    if len(interface_data) > 3: # <G>|<M>.<Y>|<D>|...'
        if interface_data[3] == 'calendar': # <G>|<M>.<Y>|<D>|calendar'
            return templates.MSG_SELECT_DAY, markups.calendar_markup(data)
        
        elif interface_data[3] == 'favorite' and len(interface_data) > 3: # <G>|<M>.<Y>|<D>|favorite|...'
            user_controller = ControllerFactory.user()
            if interface_data[4] == 'add': # <G>|<M>.<Y>|<D>|favorite|add'
                user_controller.add_favorite(callback.message.chat.id, lesson_type)

            elif interface_data[4] == 'del': # <G>|<M>.<Y>|<D>|favorite|del'
                user_controller.delete_favorite(callback.message.chat.id, lesson_type)

            data = data[:-2]
            return helpers.build_lesson_group_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)

    return None, None


def teacher_interface(
    callback: types.CallbackQuery, 
    data: List[str], 
    interface_data: List[str]
) -> Tuple[str, types.InlineKeyboardButton]:
    if len(interface_data) == 1:
        _tmp = date.today().strftime('%m.%Y|%d').split('|')
        data.extend(_tmp)
        interface_data.extend(_tmp)

    if len(interface_data) == 2: # '<T>|<M>.<Y>'
        data.append('1')
        interface_data.append('1')

    lesson_type = f'T:{interface_data[0]}'

    if len(interface_data) == 3: # '<T>|<M>.<Y>|<D>'
        return helpers.build_lesson_teacher_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)

    if len(interface_data) >= 4: # '<T>|<M>.<Y>|<D>|...'
        if interface_data[3] == 'calendar': # '<T>|<M>.<Y>|<D>|calendar'
            return templates.MSG_SELECT_DAY, markups.calendar_markup(data)

        elif interface_data[3] == 'favorite' and len(interface_data) > 4: # '<T>|<M>.<Y>|<D>|favorite|...'
            user_controller = ControllerFactory.user()
            if interface_data[4] == 'add': # '<T>|<M>.<Y>|<D>|favorite|add'
                user_controller.add_favorite(callback.message.chat.id, lesson_type)

            elif interface_data[4] == 'del': # '<T>|<M>.<Y>|<D>|favorite|del'
                user_controller.delete_favorite(callback.message.chat.id, lesson_type)

            data = data[:-2]
            return helpers.build_lesson_teacher_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)

    return None, None


def audience_interface(
    callback: types.CallbackQuery, 
    data: List[str], 
    interface_data: List[str]
) -> Tuple[str, types.ReplyKeyboardMarkup]:
    if len(interface_data) == 1: # '<A>'
        _tmp = date.today().strftime('%m.%Y|%d').split('|')
        data.extend(_tmp)
        interface_data.extend(_tmp)

    if len(interface_data) == 2: # '<A>|<M>.<Y>'
        data.append('01')
        interface_data.append('01')
    
    lesson_type = f'A:{interface_data[0]}'

    if len(interface_data) == 3: # '<A>|<M>.<Y>|<D>'
        return helpers.build_lesson_audience_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)

    if len(interface_data) >= 4: # '<A>|<M>.<Y>|<D>|...'
        if interface_data[3] == 'calendar': # '<A>|<M>.<Y>|<D>|calendar'
            return templates.MSG_SELECT_DAY, markups.calendar_markup(data)

        elif interface_data[3] == 'favorite' and len(interface_data) > 4: # '<A>|<M>.<Y>|<D>|favorite|...'
            user_controller = ControllerFactory.user()
            if interface_data[4] == 'add': # '<A>|<M>.<Y>|<D>|favorite|add'
                user_controller.add_favorite(callback.message.chat.id, lesson_type)

            elif interface_data[4] == 'del': # '<A>|<M>.<Y>|<D>|favorite|del'
                user_controller.delete_favorite(callback.message.chat.id, lesson_type)

            data = data[:-2]
            return helpers.build_lesson_audience_list(data), markups.lesson_list(data, callback.message.chat.id, lesson_type)
    
    return None, None


def group_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|') # 'group|...'
    message, markup = None, None

    if len(data) == 1: # 'group'
        message, markup = templates.MSG_SELECT_INSTITUTE, markups.institute()

    if len(data) == 2: # 'group|<I>'
        message, markup = templates.MSG_SELECT_FORM, markups.education_forms(data)

    if len(data) == 3: # 'group|<I>|<F>'
        message, markup = templates.MSG_SELECT_COURSE, markups.course(data)

    if len(data) == 4: # 'group|<I>|<F>|<C>'
        message, markup = templates.MSG_SELECT_GROUP, markups.group_list(data)

    if len(data) >= 5: # 'group|<I>|<F>|<C>|<G>|...'
        message, markup = group_interface(callback, data, data[4:])

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def teacher_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|') # 'teacher|...'
    message, markup = None, None

    if len(data) == 1:
        data.append('1')

    if len(data) == 2: # 'teacher|<P>'
        message, markup = templates.MSG_SELECT_TEACHER, markups.teacher_list(data)

    if len(data) >= 3: # 'teacher|<P>|...'
        if data[2] == 'search': # 'teacher|<P>|search...'
            if len(data) == 3: # 'teacher|<P>|search'
                msg = bot.edit_message_text(
                    templates.MSG_SEARCH_TEACHER,
                    callback.message.chat.id,
                    callback.message.id,
                    reply_markup = markups.cancle(data)
                )
                bot.register_next_step_handler(msg, helpers.search_teacher, menu_message_id=callback.message.id, bot=bot, data=data)
                message, markup = False, False
            
            if len(data) == 4: # 'teacher|<P>|search|...'
                if data[-1] == 'cancle': # 'teacher|<P>|search|cancle'
                    bot.clear_step_handler_by_chat_id(callback.message.chat.id)
                    data = data[:-2]
                    message, markup = templates.MSG_SELECT_TEACHER, markups.teacher_list(data)
            
                else: # 'teacher|<P>|search|<S>'
                    data.append('1')
            
            if len(data) == 5: # 'teacher|<P>|search|<S>|<P2>'
                message, markup = templates.MSG_SELECT_TEACHER, markups.teacher_list(data, ControllerFactory.teacher().search_by_name(data[3]), False)

    if message is None and len(data) >= 2:
        message, markup = teacher_interface(callback, data, data[2:])

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def audience_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|') # 'audience|...'
    message, markup = None, None

    if len(data) == 1: # 'audience'
        message, markup = templates.MSG_SELECT_BUILDING, markups.buildings(data)
    
    if len(data) == 2: # 'audience|<B>'
        message, markup = templates.MSG_SELECT_AUDIENCE, markups.audience_list(data)
    
    if len(data) > 2: # 'audience|<B>|...'
        message, markup = audience_interface(callback, data, data[2:])

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def favorite_callback(callback: types.CallbackQuery, bot: TeleBot):
    data = callback.data.split('|') # 'favorite|...'
    message, markup = None, None

    if len(data) == 2: # 'favorite|<T>'
        data.pop(len(data) - 1)

    if len(data) == 1: # 'favorite'
        message = templates.MSG_SELECT_FAVORITE
        markup = markups.favorite_list(
            ControllerFactory.user().get(callback.message.chat.id).get_list_favorites()
        )

    if len(data) > 2: # 'favorite|<T>|<I>|...'
        if data[1] == 'G':
            message, markup = group_interface(callback, data, data[2:])

        if data[1] == 'T':
            message, markup = teacher_interface(callback, data, data[2:])

        if data[1] == 'A':
            message, markup = audience_interface(callback, data, data[2:])

    if message:
        bot.edit_message_text(message, callback.message.chat.id, callback.message.id, reply_markup = markup)


def feedback_callback(callback: types.CallbackQuery, bot: TeleBot):
    ...


def empty_callback(callback: types.CallbackQuery, bot: TeleBot):
    pass
