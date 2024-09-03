from telebot import TeleBot
from loguru import logger

from timetable_sgugit.log import init_logger
from timetable_sgugit.services import UserDBService
from timetable_sgugit.configmodule import config


FILE_WITH_MSG_NAME = 'mailing_text.md'
EXCLUDING_CHATS = []
LOG_LVL = 'DEBUG'


def start_mailing():
    init_logger(log_lvl=LOG_LVL, write_in_file=False)
    bot = TeleBot(config.bot.token)
    EXCLUDING_CHATS.extend(map(int, config.bot.feedback_send_to.split('|')))

    with UserDBService() as service, open(FILE_WITH_MSG_NAME, 'r', encoding='utf-8') as file:
        msg_text = file.read()
        if not msg_text:
            logger.error(f'Файл с сообщением для рассылки {FILE_WITH_MSG_NAME} пустой, невозможно выполнить рассылку')
            exit(1)

        logger.info(f'Начинаем рассылку сообщения\n\nТекст сообщения:\n{msg_text}\n')
        for user in service.get_all():
            if user.chat_id in EXCLUDING_CHATS:
                logger.debug(f'Пропускаем чат id={user.chat_id}')
                continue

            logger.debug(f'Отправляем сообщение в чат id={user.chat_id} (username=@{user.username})')
            try:
                bot.send_message(user.chat_id, msg_text, parse_mode='markdown')
            except Exception as e:
                logger.error(f'Ошибка отправки сообщения в чат id={user.chat_id} (username=@{user.username}):\n({e.__class__.__name__}) {e}')
            else:
                logger.success(f'Сообщение отправлено в чат id={user.chat_id} (username=@{user.username})')
        
        logger.success('Рассылка завершена!')


if __name__ == '__main__':
    start_mailing()
