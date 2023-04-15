from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy.orm import declarative_base


engine = create_engine(f'sqlite:///timetable_sgugit.db', future=True)
Base = declarative_base()

def session_factory(**kwargs):
    return create_session(
        bind=engine,
        autocommit=False,
        autoflush=False,
        future=True,
        **kwargs
    )


from .lesson_name import LessonName
from .feedback import FeedbackSendTo
from .feedback import Feedback
from .audience import Audience
from .teacher import Teacher
from .lesson import Lesson
from .group import Group
from .user import User
