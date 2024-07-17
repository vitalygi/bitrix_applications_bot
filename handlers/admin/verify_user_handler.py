from contextlib import suppress

from aiogram import Router, flags, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.models import User
from filters.admin_filter import IsAdmin
from keyboard.user.application_keyboard import create_application
from routers.callbacks import StartCallbacksRouter
from routers.verification_user_fabric import VerificationCb, VerificationAction
from handlers.utils import change_user_state_data_key
from start.config import bot

router = Router()

@router.callback_query(VerificationCb(action=VerificationAction.verify_user).route,IsAdmin())
async def handle_start(query: CallbackQuery, dispatcher, callback_data: VerificationCb):
    user_id = callback_data.user_id
    with suppress(Exception):
        await query.message.delete()
    await User.find_one(User.id == user_id).set({'is_registered': True})
    await change_user_state_data_key(dispatcher, user_id, 'on_verification', False)
    await bot.send_message(chat_id=user_id, text='Доступ к боту разрешен', reply_markup=create_application())
