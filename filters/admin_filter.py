from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from start.config import admins


class IsAdmin(Filter):
    """
        Фильтр для проверки является ли юзер админом
    """
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return message.from_user.id in admins
