from typing import Optional, List

from sqlalchemy import and_

from .abc import BaseService
from ..orm import Group


class GroupDBService(BaseService[Group]):

    def get_by_name(self, name: str) -> Optional[Group]:
        return self.get_filtered_first(Group.name == name)


    def get_by_filter(
        self,
        institute: Optional[int] = None,
        education_form: Optional[int] = None,
        course: Optional[int] = None,
    ) -> List[Group]:
        _filter = True

        if institute is not None:
            _filter = and_(_filter, Group.institute == institute)
        if education_form is not None:
            _filter = and_(_filter, Group.education_form == education_form)
        if course is not None:
            _filter = and_(_filter, Group.course == course)

        return self.get_filtered(_filter)
