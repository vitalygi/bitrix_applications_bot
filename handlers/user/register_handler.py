import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.models import User
from filters.register_filter import IsRegistered
from filters.verification_filter import IsOnVerification, NotRegisteredYet
from handlers.utils.admin_utils import send_register_user_application_to_group
from handlers.utils.utils import change_state_key

router = Router()
router.message.filter(IsRegistered(False))


class EnterRegisterData(StatesGroup):
    ENTER_NAME = State()


@router.message(EnterRegisterData.ENTER_NAME)
@router.message(IsOnVerification())
async def handle_verification(message: Message, state: FSMContext, user: User):
    handler_state = await state.get_state()
    if handler_state == EnterRegisterData.ENTER_NAME:
        user.register_date = datetime.datetime.now().strftime('%d.%m.%Y')
        user.name = message.text
        await user.save()
        await send_register_user_application_to_group(user)
        await state.set_state(None)
        await change_state_key(state, 'on_verification', True)
    await message.answer(
        'Ваш аккаунт ждет подтверждения администратора. Я напишу Вам, когда администратор подтвердит доступ')


@router.message(Command('start'), IsOnVerification(False),NotRegisteredYet())
async def handle_start(message: Message, state: FSMContext):
    await state.set_state(EnterRegisterData.ENTER_NAME)
    await message.answer('Введите ФИО')
