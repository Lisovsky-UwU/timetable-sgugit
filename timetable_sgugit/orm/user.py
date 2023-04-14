from typing import List
from typing import Tuple
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer

from . import Base


class User(Base):

    __tablename__ = 'users'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    chat_id    = Column(Integer, nullable=False)
    username   = Column(String, nullable=False)
    favorites  = Column(String, nullable=False, default='') # G:100|T:32|A:6


    def get_list_favorites(self) -> List[Tuple[str, str]]:
        return list(
            tuple(fav.split(':'))
            for fav in self.favorites.split('|')
        )
