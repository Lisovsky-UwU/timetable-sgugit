from typing import Optional
from sqlalchemy import and_

from .abc import BaseService
from ..orm import User


class UserDBService(BaseService[User]):

    def get_for_filter(self, chat_id: Optional[int] = None, username: Optional[str] = None) -> Optional[User]:
        _filter = True

        if chat_id is not None:
            _filter = and_(_filter, User.chat_id == chat_id)
        
        if username is not None:
            _filter = and_(_filter, User.username == username)

        return self.get_filtered_first(_filter)
