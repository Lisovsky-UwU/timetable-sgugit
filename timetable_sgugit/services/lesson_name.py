from typing import Optional

from .abc import BaseService
from ..orm import LessonName


class LessonNameDBService(BaseService[LessonName]):

    def get_by_name(self, name: str) -> Optional[LessonName]:
        return self.get_filtered_first(LessonName.name == name)
