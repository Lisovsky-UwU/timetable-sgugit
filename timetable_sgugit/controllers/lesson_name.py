from typing import Type
from functools import lru_cache

from ..services import LessonNameDBService
from ..orm import LessonName


class LessonNameDBController:

    def __init__(self, service_type: Type[LessonNameDBService]):
        self.service_type = service_type


    def clear_table(self):
        with self.service_type() as service:
            service.delete_for_list(service.get_all())
            service.commit()


    @lru_cache(maxsize=None)
    def create_if_not_exists(self, name: str) -> LessonName:
        with self.service_type() as service:
            data = service.get_by_name(name)
            if data is None:
                data = service.create(LessonName(name = name))
                service.commit()

            return data
