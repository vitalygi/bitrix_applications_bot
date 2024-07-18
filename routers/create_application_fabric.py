from enum import Enum
from typing import Optional

from aiogram import F
from aiogram.filters.callback_data import CallbackData


class ApplicationAction(Enum):
    start_creation = '1'
    enter_direction = '2'
    enter_pay_form = '5'
    enter_payer = '3'
    back = '4'
    # will not contain data
    enter_responsible = '6'
    enter_comments = '7'
    enter_amount = '8'
    enter_article = '9'
    enter_payment_date = '10'
    enter_add_info = '11'
    enter_file = '12'
    check_application='13'
    send_application = '14'

class ApplicationCb(CallbackData, prefix="create_application"):
    action: ApplicationAction
    user_id: Optional[int] = None
    answer: Optional[str] = None
    back: Optional[str] = None

    @property
    def route(self):
        return self.filter(F.action == self.action)

    @property
    def back_route(self):
        return self.filter(F.action == self.action and F.back == self.back)

    def with_user_id(self, user_id: str | int):
        self.user_id = int(user_id)
        return self

    def with_answer(self, answer: str):
        self.answer = answer
        return self


