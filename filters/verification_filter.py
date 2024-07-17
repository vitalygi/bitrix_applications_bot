from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from start.config import admins


class IsOnVerification(Filter):
    """
        Фильтр для проверки стоит ли пользователь в очереди на верификацию
    """

    def __init__(self, is_on_verification: bool = True):
        self.is_on_verification = is_on_verification

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        data = await state.get_data()
        is_on_verification = data.get('on_verification', False)
        return is_on_verification == self.is_on_verification
