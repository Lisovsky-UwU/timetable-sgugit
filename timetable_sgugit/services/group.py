from typing import Optional

from .abc import BaseService
from ..orm import Group


class GroupDBService(BaseService[Group]):

    def get_by_name(self, name: str) -> Optional[Group]:
        return self.get_filtered_first(Group.name == name)
