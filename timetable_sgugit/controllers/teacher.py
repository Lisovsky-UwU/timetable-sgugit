from typing import Type
from typing import List
from typing import Iterable
from functools import lru_cache

from ..services import TeacherDBService
from ..orm import Teacher


class TeacherDBController:

    def __init__(self, service_type: Type[TeacherDBService]):
        self.service_type = service_type


    def fill_for_iter(self, payload: Iterable[str]) -> List[Teacher]:
        with self.service_type() as service:
            service.delete_for_list(service.get_all())
            data = service.create_for_iter(
                Teacher(name = data)
                for data in payload
            )
            service.commit()

            return data


    @lru_cache(maxsize=None)
    def create_if_not_exists(self, name: Iterable[str]) -> Teacher:
        with self.service_type() as service:
            data = service.get_by_name(name)
            if data is None:
                data = service.create(Teacher(name = name))
                service.commit()

            return data
