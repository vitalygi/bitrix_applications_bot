from enum import Enum
from typing import Optional

from aiogram import F
from aiogram.filters.callback_data import CallbackData


class ApplicationAction(Enum):
    start_creation = '1'
    enter_direction = '2'
    enter_payer = '3'
    back = '4'


class ApplicationCb(CallbackData, prefix="create_application"):
    action: ApplicationAction
    user_id: Optional[int] = None
    answer: Optional[str] = None

    @property
    def route(self):
        return self.filter(F.action == self.action)

    def with_user_id(self, user_id: str | int):
        self.user_id = int(user_id)
        return self

    def with_answer(self, answer: str):
        self.answer = answer
        return self


