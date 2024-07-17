from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from start.config import managers


class IsManager(Filter):
    """
        Фильтр для проверки является ли юзер менеджером
    """
    async def __call__(self, message) -> bool:
        return message.from_user.id in managers