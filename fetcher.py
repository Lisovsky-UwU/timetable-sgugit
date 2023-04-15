import argparse


if __name__ == '__main__':
    try:
        arg_parser = argparse.ArgumentParser(
            description="Script for forced fetching informations", 
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        arg_parser.add_argument('-a', '--all', action='store_true', help='fetch all')
        arg_parser.add_argument('-g', '--groups', action='store_true', help='fetch groups')
        arg_parser.add_argument('-t', '--teachers', action='store_true', help='fetch teachers')
        arg_parser.add_argument('-u', '--audience', action='store_true', help='fetch audience')
        arg_parser.add_argument('-l', '--lessons', action='store_true', help='fetch lessons')
        config = vars(arg_parser.parse_args())

        if any(config.values()):
            from timetable_sgugit.log import init_logger
            from timetable_sgugit.utils import create_db
            from timetable_sgugit.factory import ControllerFactory
            from timetable_sgugit.services import GroupDBService
            from timetable_sgugit.services import LessonDBService
            from timetable_sgugit.services import TeacherDBService
            from timetable_sgugit.services import AudienceDBService
            from timetable_sgugit.services import LessonNameDBService

            ControllerFactory.group_service_type = GroupDBService
            ControllerFactory.lesson_service_type = LessonDBService
            ControllerFactory.teacher_service_type = TeacherDBService
            ControllerFactory.audience_service_type = AudienceDBService
            ControllerFactory.lesson_name_service_type = LessonNameDBService

            init_logger()
            create_db()

            if config['all']:
                ControllerFactory.data_fetcher().fetch_all()
            else:
                if config['groups']:
                    ControllerFactory.data_fetcher().fetch_groups()
                if config['teachers']:
                    ControllerFactory.data_fetcher().fetch_teachers()
                if config['audience']:
                    ControllerFactory.data_fetcher().fetch_audiences()
                if config['lessons']:
                    ControllerFactory.data_fetcher().fetch_lessons()
    
    except KeyboardInterrupt:
        print('Принудительное завершение работы скрипта')
