from typing import Tuple, Type

from ..services import FeedbackSendToDBService, FeedbackDBService
from ..orm import FeedbackSendTo, Feedback


class FeedbackDBController:

    def __init__(
        self,
        feedback_service_type: Type[FeedbackDBService],
        feedback_send_to_service_type: Type[FeedbackSendToDBService]
    ):
        self.feedback_service_type = feedback_service_type
        self.feedback_send_to_service_type = feedback_send_to_service_type


    def take_feedback(self, user_id: int, message_id: int) -> Feedback:
        with self.feedback_service_type() as fb_service:
            feedback_db = fb_service.create(
                Feedback(
                    user = user_id,
                    message_id = message_id,
                )
            )

            fb_service.commit()
            return feedback_db
        
    
    def send_feedback_to(self, user_id: int, message_id: int, feedback_id: int) -> FeedbackSendTo:
        with self.feedback_send_to_service_type() as fb_st_service:
            fb_st_db = fb_st_service.create(
                FeedbackSendTo(
                    user = user_id,
                    message_id = message_id,
                    feedback = feedback_id
                )
            )

            fb_st_service.commit()
            return fb_st_db
        
    
    def reply_to(self, user_id: int, to_msg_id: int) -> Tuple[int, str]:
        with self.feedback_send_to_service_type() as fb_st_service:
            fb_st_db = fb_st_service.get_for_user_and_msg(user_id, to_msg_id)
            return fb_st_db.feedback_db.user_db.chat_id, fb_st_db.feedback_db.message_id
