from typing import List
from typing import Optional
from sqlalchemy import and_

from .abc import BaseService
from ..orm import Lesson


class LessonDBService(BaseService[Lesson]):

    def get_by_filter(
        self,
        group: Optional[int] = None,
        audience: Optional[int] = None,
        teacher: Optional[int] = None,
        date: Optional[str] = None,
    ) -> List[Lesson]:
        _filter = True

        if group is not None:
            _filter = and_(_filter, Lesson.group == group)
        if audience is not None:
            _filter = and_(_filter, Lesson.audience == audience)
        if teacher is not None:
            _filter = and_(_filter, Lesson.teacher == teacher)
        if date is not None:
            _filter = and_(_filter, Lesson.date == date)

        return self.get_filtered(_filter)
