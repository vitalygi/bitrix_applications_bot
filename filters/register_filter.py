from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update

from data.models import User
from start.config import managers


class IsRegistered(Filter):
    """
        Фильтр для проверки является ли юзер зарегестрированным
    """

    def __init__(self, is_registered: bool = True):
        self.is_registered = is_registered


    #get data injected in middleware in filter
    async def __call__(self, *args, **kwargs) -> bool:
        update: Update = kwargs.get('event_update')
        return update.is_registered == self.is_registered
