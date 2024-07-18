from enum import Enum
from typing import Optional

from aiogram import F
from aiogram.filters.callback_data import CallbackData


class AdminAction(Enum):
    all_users = '1'
    enter_id = '2'
    menu = '3'

class AdminCb(CallbackData, prefix="admin_menu"):
    action: AdminAction
    user_id: Optional[int] = None

    @property
    def route(self):
        return self.filter(F.action == self.action)

    def with_user_id(self, user_id: str | int):
        self.user_id = int(user_id)
        return self

