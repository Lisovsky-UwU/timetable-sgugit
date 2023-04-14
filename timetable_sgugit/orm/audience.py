from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from . import Base


class Audience(Base):

    __tablename__ = 'audiences'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, nullable=False)
    building   = Column(Integer, nullable=False)

    lessons_db = relationship('Lesson', back_populates='audience_db', uselist=True)
