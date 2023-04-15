from typing import Optional
from sqlalchemy import and_

from .abc import BaseService
from ..orm import Feedback
from ..orm import FeedbackSendTo


class FeedbackDBService(BaseService[Feedback]):

    ...


class FeedbackSendToDBService(BaseService[FeedbackSendTo]):

    def get_for_user_and_msg(self, user_id: int, message_id: int) -> Optional[FeedbackSendTo]:
        return self.get_filtered_first(
            and_(
                FeedbackSendTo.user == user_id,
                FeedbackSendTo.message_id == message_id
            )
        )
