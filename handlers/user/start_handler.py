from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from filters.register_filter import IsRegistered

router = Router()


@router.message(Command('start'),IsRegistered())
async def handle_start(message: Message, state: FSMContext):
    await message.answer('Привет, пользователь')


