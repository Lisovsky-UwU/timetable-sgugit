from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Lesson(Base):

    __tablename__ = 'lessons'

    id             = Column(Integer, primary_key=True, autoincrement=True)
    hour           = Column(Integer, nullable=False)
    lesson_type    = Column(Integer, nullable=False)
    audience       = Column(String, nullable=True, index=True)
    group          = Column(Integer, ForeignKey('groups.id'), nullable=False, index=True)
    teacher        = Column(Integer, ForeignKey('teachers.id'), nullable=False, index=True)
    lesson_name    = Column(Integer, ForeignKey('lesson_names.id'), nullable=False)
    date           = Column(String, nullable=False, index=True)

    group_db       = relationship('Group', back_populates='lessons_db', uselist=False)
    teacher_db     = relationship('Teacher', back_populates='lessons_db', uselist=False)
    lesson_name_db = relationship('LessonName', back_populates='lessons_db', uselist=False)
