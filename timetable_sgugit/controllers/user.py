from typing import Type
from typing import Optional
from functools import lru_cache

from ..services import UserDBService
from ..orm import User


class UserDBController:

    def __init__(self, service_type: Type[UserDBService]):
        self.service_type = service_type


    def get(self, chat_id: Optional[int] = None, username: Optional[str] = None) -> Optional[User]:
        with self.service_type() as service:
            return service.get_for_filter(chat_id, username)


    def add_favorite(self, chat_id: int, data: str):
        with self.service_type() as service:
            user = self.get(chat_id)
            if data in user.favorites:
                return
            
            favorites_list = user.favorites.split('|') if user.favorites != '' else list()
            favorites_list.append(data)

            user.favorites = '|'.join(favorites_list)
            service.update(user)
            service.commit()


    def delete_favorite(self, chat_id: int, data: str):
        with self.service_type() as service:
            user = self.get(chat_id)
            if data not in user.favorites:
                return
            
            favorites_list = user.favorites.split('|')
            favorites_list.remove(data)

            user.favorites = '|'.join(favorites_list)
            service.update(user)
            service.commit()


    @lru_cache(maxsize=None)
    def create_if_not_exists(self, chat_id: int, username: str) -> User:
        with self.service_type() as service:
            data = service.get_for_filter(chat_id, username)
            if data is None:
                data = service.create(
                    User(
                        username = username,
                        chat_id  = chat_id
                    )
                )
                service.commit()

            return data
