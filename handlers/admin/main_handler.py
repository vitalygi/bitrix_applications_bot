from contextlib import suppress
from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from handlers.utils.admin_utils import save_users_to_file
from states.admin.admin import AdminStatesGroup
from filters.admin_filter import IsAdmin
from keyboard.admin.main_menu import *

router = Router()





@router.message(Command('start'), IsAdmin())
@router.callback_query(AdminCb(action=AdminAction.menu).route)
async def handle_start(message: Message, state: FSMContext):
    if isinstance(message, CallbackQuery):
        message = message.message
    await state.clear()
    await message.answer('Вы администратор бота', reply_markup=main_menu())


@router.callback_query(AdminCb(action=AdminAction.all_users).route)
async def handle_all_users(query: CallbackQuery):
    await query.answer()
    users = await User.find().to_list()
    save_users_to_file(users)
    document = FSInputFile('users.xlsx')
    await query.bot.send_document(chat_id=query.from_user.id, document=document, caption='Все пользователи')


@router.callback_query(AdminCb(action=AdminAction.enter_id).route)
@flags.del_from
async def handle_enter_id(query: CallbackQuery, state: FSMContext):
    await query.message.answer('Введите ID пользователя')
    await state.set_state(AdminStatesGroup.enter_id)


@router.message(AdminStatesGroup.enter_id, F.text)
async def handle_entered_id(message: Message):
    user_id = message.text
    try:
        user = await User.find_one(User.id == int(user_id))
        if user.is_registered:
            user.is_registered = False
            add_info = f'Пользователь {user.id}, {user.name} заблокирован'
            user_add_info = 'Доступ к боту запрещён'
        else:
            user.is_registered = True
            add_info = f'Пользователь {user.id}, {user.name} разблокирован'
            user_add_info = 'Доступ к боту разрешён'
        await user.save()
        await message.answer(f'{add_info}\nВы можете продолжить ввод ID или вернуться в меню', reply_markup=back_menu())
        with suppress(Exception):
            await message.bot.send_message(chat_id=user.id, text=user_add_info)
    except:
        await message.answer(f'Пользователь не был найден\nВы можете продолжить ввод ID или вернуться в меню',
                             reply_markup=back_menu())
