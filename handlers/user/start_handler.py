from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(Command('start'))
async def handle_start(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(data.get('text', 'no text'))


@router.message()
async def handle_start(message: Message, state: FSMContext):
    await state.set_data({'text': message.text})


@router.message(Command('bye'))
@flags.del_from
async def handle_bye(message: Message):
    await message.answer('bye')
