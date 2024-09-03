from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from . import Base


class Teacher(Base):

    __tablename__ = 'teachers'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, nullable=False)

    lessons_db = relationship('Lesson', back_populates='teacher_db', uselist=True)
