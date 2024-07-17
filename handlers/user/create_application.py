from typing import Optional, List

from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.models import User
from filters.register_filter import IsRegistered
from filters.verification_filter import IsOnVerification
from handlers.admin_utils import send_register_user_application_to_group
from handlers.utils import change_state_key
from keyboard.user.application_keyboard import choose_direction_kb
from routers.create_application_fabric import *
from handlers.utils import change_state_key

router = Router()

responsible: Optional[str] = ''
direction: Optional[str] = ''
pay_form: Optional[str] = ''
payer: Optional[str] = ''
article: Optional[str] = ''
comments: Optional[str] = ''
amount: int
payment_date: Optional[str] = ''
add_info: Optional[str] = ''
files: Optional[List[str]] = []


class Application(StatesGroup):
    enter_responsible = State()
    enter_comments = State()
    enter_amount = State()
    enter_article = State()
    enter_payment_date = State()
    enter_add_info = State()


@router.callback_query(ApplicationCb(action=ApplicationAction.start_creation).route)
@router.callback_query(ApplicationCb(action=ApplicationAction.back).filter(F.answer == 'responsible'))
@flags.del_from()
async def start_application_creation(query: CallbackQuery, user: User, state: FSMContext):
    print(F.action==ApplicationAction.start_creation)
    a = 1
    await query.message.answer('Введите ответственного:')
    await state.set_state(Application.enter_responsible)


@router.message(Application.enter_responsible)
@router.callback_query(ApplicationCb(action=ApplicationAction.back).filter(F.answer == 'direction'))
@flags.del_from()
async def enter_responsible_handler(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        await change_state_key(state, 'responsible', message.text)
    await message.answer(text='Выберите направление', reply_markup=choose_direction_kb())
