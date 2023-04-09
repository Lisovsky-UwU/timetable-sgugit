from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import relationship

from . import Base


class LessonName(Base):

    __tablename__ = 'lesson_names'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, nullable=False)

    lessons_db = relationship('Lesson', back_populates='lesson_name_db', uselist=True)
