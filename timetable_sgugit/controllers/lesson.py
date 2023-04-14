from typing import Type
from typing import List
from typing import Iterable
from typing import Optional

from ..constants import HOURS_TYPE
from ..services import LessonDBService
from ..models import LessonAddRequest
from ..models import LessonInfoModel
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


    def get(
        self,
        group: Optional[int] = None,
        audience: Optional[str] = None,
        teacher: Optional[int] = None,
        date: Optional[str] = None,
    ) -> List[LessonInfoModel]:
        with self.service_type() as service:
            lesson_list = list(
                LessonInfoModel(
                    id          = lesson.id,
                    hour        = lesson.hour,
                    lesson_type = lesson.lesson_type,
                    audience    = lesson.audience,
                    group       = lesson.group_db.name,
                    teacher     = lesson.teacher_db.name,
                    lesson_name = lesson.lesson_name_db.name,
                    date        = lesson.date
                )
                for lesson in sorted(service.get_by_filter(group, audience, teacher, date), key=lambda l: l.hour)
            )

            # Сломается, если в однов время занятия будут в разных аудиториях
            # отобразится только первая аудитория для всех групп
            # Но такого в расписании (вроде) не бывает
            result = list()
            for hour in HOURS_TYPE:
                _lessons = list(filter(lambda l: l.hour == hour, lesson_list))
                if len(_lessons) == 1:
                    result.append(_lessons[0])

                elif len(_lessons) > 1:
                    r_lesson = _lessons[0]
                    for lesson in _lessons[1:]:
                        if lesson.group not in r_lesson.group:
                            r_lesson.group += f', {lesson.group}'

                    result.append(r_lesson)
            
            return result
