from typing import Type
from typing import List
from typing import Iterable
from functools import lru_cache

from ..services import AudienceDBService
from ..models import AudienceCreateRequest
from ..orm import Audience


class AudienceDBController:

    def __init__(self, service_type: Type[AudienceDBService]):
        self.service_type = service_type


    def get_all(self) -> List[Audience]:
        with self.service_type() as service:
            return service.get_all()


    @lru_cache(maxsize=None)
    def create_if_not_exists(self, name: str) -> Audience:
        with self.service_type() as service:
            data = service.get_by_name(name)
            if data is None:
                data = service.create(
                    Audience(
                        name     = name,
                        building = 0,
                    )
                )

            return data


    def fill_for_iter(self, payload: Iterable[AudienceCreateRequest]) -> List[Audience]:
        with self.service_type() as service:
            service.delete_for_list(service.get_all())
            data = service.create_for_iter(
                Audience(
                    name     = data.name,
                    building = data.building,
                )
                for data in payload
            )
            service.commit()

            return data
