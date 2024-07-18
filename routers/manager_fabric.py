from enum import Enum
from typing import Optional

from aiogram import F
from aiogram.filters.callback_data import CallbackData


class ManagerAction(Enum):
    all_applications = '1'
    verify_application = '2'
    block_application = '3'


class ManagerCb(CallbackData, prefix="manager"):
    action: ManagerAction
    user_id: Optional[int] = None
    answer: Optional[str] = None
    @property
    def route(self):
        return self.filter(F.action == self.action)

    def with_user_id(self, user_id: str | int):
        self.user_id = int(user_id)
        return self
