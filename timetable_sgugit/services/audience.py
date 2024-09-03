from typing import Optional, List

from .abc import BaseService
from ..orm import Audience


class AudienceDBService(BaseService[Audience]):

    def get_by_name(self, name: str) -> Optional[Audience]:
        return self.get_filtered_first(Audience.name == name)

    
    def get_by_building(self, building: int) -> List[Audience]:
        return self.get_filtered(Audience.building == building)
