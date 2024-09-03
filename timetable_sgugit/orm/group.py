from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from . import Base


class Group(Base):

    __tablename__ = 'groups'

    id             = Column(Integer, primary_key=True, autoincrement=True)
    sgugit_id      = Column(Integer, nullable=False)
    name           = Column(String, nullable=False, index=True)
    course         = Column(Integer, nullable=False, index=True)
    institute      = Column(Integer, nullable=False, index=True)
    education_form = Column(Integer, nullable=False, index=True)

    lessons_db     = relationship('Lesson', back_populates='group_db', uselist=True)
