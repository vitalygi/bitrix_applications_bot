from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from filters.admin_filter import IsAdmin
from filters.register_filter import IsRegistered

router = Router()


@router.message(Command('admin'),IsAdmin())
async def handle_start(message: Message):
    await message.answer('Hey Admin')

