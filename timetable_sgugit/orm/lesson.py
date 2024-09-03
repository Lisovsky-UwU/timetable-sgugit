from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Lesson(Base):

    __tablename__ = 'lessons'

    id             = Column(Integer, primary_key=True, autoincrement=True)
    hour           = Column(Integer, nullable=False)
    lesson_type    = Column(Integer, nullable=False)
    audience       = Column(Integer, ForeignKey('audiences.id'), nullable=True, index=True)
    group          = Column(Integer, ForeignKey('groups.id'), nullable=True, index=True)
    teacher        = Column(Integer, ForeignKey('teachers.id'), nullable=True, index=True)
    lesson_name    = Column(Integer, ForeignKey('lesson_names.id'), nullable=False)
    date           = Column(String, nullable=False, index=True)

    group_db       = relationship('Group', back_populates='lessons_db', uselist=False)
    teacher_db     = relationship('Teacher', back_populates='lessons_db', uselist=False)
    audience_db    = relationship('Audience', back_populates='lessons_db', uselist=False)
    lesson_name_db = relationship('LessonName', back_populates='lessons_db', uselist=False)
