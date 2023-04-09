from typing import Type
from typing import Iterable

from ..services import LessonDBService
from ..models import LessonAddRequest
from ..orm import Lesson


class LessonDBController:

    def __init__(self, service_type: Type[LessonDBService]):
        self.service_type = service_type


    def fill_table(self, payload: Iterable[LessonAddRequest]) -> Lesson:
        with self.service_type() as service:
            service.delete_for_list(service.get_all())
            data = service.create_for_iter(
                Lesson(
                    hour        = data.hour_id,
                    lesson_type = data.lesson_type_id,
                    audience    = data.audience,
                    group       = data.group_id,
                    teacher     = data.teacher_id,
                    lesson_name = data.lesson_name_id,
                    date        = data.date
                )
                for data in payload
            )
            service.commit()

            return data
