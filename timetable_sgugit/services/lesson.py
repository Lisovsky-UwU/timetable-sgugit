from .abc import BaseService
from ..orm import Lesson


class LessonDBService(BaseService[Lesson]):

    ...
