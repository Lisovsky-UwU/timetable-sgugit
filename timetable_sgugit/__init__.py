from .services import LessonNameDBService
from .services import TeacherDBService
from .services import LessonDBService
from .services import GroupDBService
from .factory import ControllerFactory
from .utils import create_db
from .log import init_logger
from .bot import build_bot


def start():
    try:
        init_logger()
        create_db()
        
        ControllerFactory.group_service_type = GroupDBService
        ControllerFactory.lesson_service_type = LessonDBService
        ControllerFactory.teacher_service_type = TeacherDBService
        ControllerFactory.lesson_name_service_type = LessonNameDBService
        
        # ControllerFactory.data_fetcher().fetch_groups()
        # ControllerFactory.data_fetcher().fetch_teachers()
        # ControllerFactory.data_fetcher().fetch_lessons()

        build_bot().infinity_polling()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    start()
