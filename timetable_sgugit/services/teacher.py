from typing import List, Optional

from .abc import BaseService
from ..orm import Teacher


class TeacherDBService(BaseService[Teacher]):

    def get_by_name(self, name: str) -> Optional[Teacher]:
        return self.get_filtered_first(Teacher.name == name)


    def search_by_name(self, name: str) -> List[Teacher]:
        return self.get_filtered(Teacher.name.contains(name))
