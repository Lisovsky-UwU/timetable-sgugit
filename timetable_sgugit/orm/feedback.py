from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Feedback(Base):

    __tablename__ = 'feedbacks'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    user       = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    message_id = Column(Integer, nullable=False)

    user_db             = relationship('User', back_populates='feedbacks_db', uselist=False)
    feedback_send_to_db = relationship('FeedbackSendTo', back_populates='feedback_db', uselist=True)


class FeedbackSendTo(Base):

    __tablename__ = 'feedbacks_send_to'

    id         = Column(Integer, primary_key=True, autoincrement=True)
    user       = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)
    message_id = Column(Integer, nullable=False)
    feedback   = Column(Integer, ForeignKey('feedbacks.id'), nullable=True, index=True)

    user_db     = relationship('User', back_populates='feedbacks_send_to_db', uselist=False)
    feedback_db = relationship('Feedback', back_populates='feedback_send_to_db', uselist=False)
