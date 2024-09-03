from typing import Type

from .parser import SgugitWebParser
from .services import (
    UserDBService,
    GroupDBService,
    LessonDBService,
    TeacherDBService,
    AudienceDBService,
    LessonNameDBService,
    FeedbackDBService,
    FeedbackSendToDBService
)
from .controllers import (
    DataFetcher,
    UserDBController,
    GroupDBController,
    LessonDBController,
    TeacherDBController,
    AudienceDBController,
    FeedbackDBController,
    LessonNameDBController
)


class ControllerFactory:
    
    user_service_type: Type[UserDBService]
    group_service_type: Type[GroupDBService]
    lesson_service_type: Type[LessonDBService]
    teacher_service_type: Type[TeacherDBService]
    audience_service_type: Type[AudienceDBService]
    lesson_name_service_type: Type[LessonNameDBService]
    feedback_service_type: Type[FeedbackDBService]
    feedback_send_to_service_type: Type[FeedbackSendToDBService]

    
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
    def feedback(cls):
        return FeedbackDBController(
            cls.feedback_service_type,
            cls.feedback_send_to_service_type
        )


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
