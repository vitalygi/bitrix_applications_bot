from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.models import User
from filters.register_filter import IsRegistered
from filters.verification_filter import IsOnVerification
from handlers.admin_utils import send_register_user_application_to_group
from handlers.utils import change_state_key

router = Router()


class EnterRegisterData(StatesGroup):
    ENTER_NAME = State()

@router.message(EnterRegisterData.ENTER_NAME, IsRegistered(False))
@router.message(IsOnVerification())
async def handle_verification(message: Message, state: FSMContext, user: User):
    handler_state = await state.get_state()
    if handler_state == EnterRegisterData.ENTER_NAME:
        user.name = message.text
        await user.save()
        await send_register_user_application_to_group(user)
        await state.set_state(None)
        await change_state_key(state, 'on_verification', True)
    await message.answer('Ваш аккаунт ждет подтверждения администратора. Я напишу Вам, когда администратор подтвердит доступ')

@router.message(Command('start'), IsRegistered(False),IsOnVerification(False))
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(EnterRegisterData.ENTER_NAME)
    await message.answer('Введите ФИО')


