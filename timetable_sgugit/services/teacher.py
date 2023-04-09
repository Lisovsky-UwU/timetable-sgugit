from typing import Optional

from .abc import BaseService
from ..orm import Teacher


class TeacherDBService(BaseService[Teacher]):

    def get_by_name(self, name: str) -> Optional[Teacher]:
        return self.get_filtered_first(Teacher.name == name)
