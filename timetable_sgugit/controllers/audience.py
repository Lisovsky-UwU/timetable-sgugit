from typing import Type
from typing import List

from ..services import AudienceDBService
from ..orm import Audience


class AudienceDBController:

    def __init__(self, service_type: Type[AudienceDBService]):
        self.service_type = service_type


    def get_all(self) -> List[Audience]:
        with self.service_type() as service:
            return service.get_all()
