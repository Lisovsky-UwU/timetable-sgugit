from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from . import Base


class Group(Base):

    __tablename__ = 'groups'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, nullable=False)

    lessons_db = relationship('Lesson', back_populates='group_db', uselist=True)
