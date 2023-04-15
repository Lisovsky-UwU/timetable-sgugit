from loguru import logger

from .fetch_manager import FetchManager
from .configmodule import config
from .services import FeedbackSendToDBService
from .services import FeedbackDBService
from .services import LessonNameDBService
from .services import AudienceDBService
from .services import TeacherDBService
from .services import LessonDBService
from .services import GroupDBService
from .services import UserDBService
from .factory import ControllerFactory
from .utils import create_db
from .log import init_logger
from .bot import build_bot


def start():
    try:
        init_logger()
        create_db()
        
        ControllerFactory.user_service_type = UserDBService
        ControllerFactory.group_service_type = GroupDBService
        ControllerFactory.lesson_service_type = LessonDBService
        ControllerFactory.teacher_service_type = TeacherDBService
        ControllerFactory.audience_service_type = AudienceDBService
        ControllerFactory.lesson_name_service_type = LessonNameDBService
        ControllerFactory.feedback_service_type = FeedbackDBService
        ControllerFactory.feedback_send_to_service_type = FeedbackSendToDBService
        
        if config.parser.manager:
            logger.info('Запуск FetchManager')
            fetch_manager = FetchManager(
                ControllerFactory.data_fetcher()
            )
            fetch_manager.start()
            logger.success('FetchManager запущен')
        else:
            logger.info('FetchManager выключен настройками конфигурации')

        logger.info('Запуск бота')
        build_bot().infinity_polling()

    except KeyboardInterrupt:
        fetch_manager.join()


if __name__ == '__main__':
    start()
