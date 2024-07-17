from enum import Enum
from typing import Optional

from aiogram import F
from aiogram.filters.callback_data import CallbackData


class VerificationAction(Enum):
    verify_user = '1'
    block_user = '2'


class VerificationCb(CallbackData, prefix="verify_register"):
    action: VerificationAction
    user_id: Optional[int] = None

    @property
    def route(self):
        return self.filter(F.action == self.action)

    def with_user_id(self, user_id: str | int):
        self.user_id = int(user_id)
        return self

