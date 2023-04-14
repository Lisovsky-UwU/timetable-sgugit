from typing import Type

from .parser import SgugitWebParser
from .services import UserDBService
from .services import GroupDBService
from .services import LessonDBService
from .services import TeacherDBService
from .services import AudienceDBService
from .services import LessonNameDBService
from .controllers import DataFetcher
from .controllers import UserDBController
from .controllers import GroupDBController
from .controllers import LessonDBController
from .controllers import TeacherDBController
from .controllers import AudienceDBController
from .controllers import LessonNameDBController


class ControllerFactory:
    
    user_service_type: Type[UserDBService]
    group_service_type: Type[GroupDBService]
    lesson_service_type: Type[LessonDBService]
    teacher_service_type: Type[TeacherDBService]
    audience_service_type: Type[AudienceDBService]
    lesson_name_service_type: Type[LessonNameDBService]

    
    @classmethod
    def group(cls):
        return GroupDBController(cls.group_service_type)
    
    
    @classmethod
    def lesson(cls):
        return LessonDBController(cls.lesson_service_type)
    
    
    @classmethod
    def teacher(cls):
        return TeacherDBController(cls.teacher_service_type)
    
    
    @classmethod
    def lesson_name(cls):
        return LessonNameDBController(cls.lesson_name_service_type)
    

    @classmethod
    def audience(cls):
        return AudienceDBController(cls.audience_service_type)


    @classmethod
    def user(cls):
        return UserDBController(cls.user_service_type)


    @classmethod
    def data_fetcher(cls):
        return DataFetcher(
            SgugitWebParser(),
            cls.group(),
            cls.lesson(),
            cls.teacher(),
            cls.audience(),
            cls.lesson_name(),
        )
