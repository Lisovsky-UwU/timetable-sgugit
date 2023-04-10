from typing import Type
from typing import List
from typing import Optional
from typing import Iterable

from ..services import GroupDBService
from ..models import GroupCreateRequest
from ..orm import Group


class GroupDBController:

    def __init__(self, service_type: Type[GroupDBService]):
        self.service_type = service_type


    def get_by_id(self, id: int):
        with self.service_type() as service:
            return service.get_by_id(id)


    def get(
        self,
        institute: Optional[int] = None,
        education_form: Optional[int] = None,
        course: Optional[int] = None
    ) -> List[Group]:
        with self.service_type() as service:
            return service.get_by_filter(institute, education_form, course)


    def fill_for_iter(self, payload: Iterable[GroupCreateRequest]) -> List[Group]:
        with self.service_type() as service:
            service.delete_for_list(service.get_all())

            data = service.create_for_iter(
                Group(
                    sgugit_id      = data.sgugit_id,
                    name           = data.name,
                    course         = data.course,
                    institute      = data.institute,
                    education_form = data.education_form
                )
                for data in payload
            )
            service.commit()

            return data
