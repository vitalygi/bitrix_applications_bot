import logging

from aiogram import Router, flags
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from data.models import Application
from data.send_to_bitrix import send_application_to_bitrix
from handlers.utils.utils import notify_admins_and_managers
from keyboard.manager.verify_application_keyboard import all_applications
from routers.manager_fabric import *
from start.config import bot
from handlers.utils.manager_utils import render_application_to_check

router = Router()


@router.message(Command('start'))
async def handle_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вы являетесь руководителем бота, тут будут отображаться заявки на согласование документов',
                         reply_markup=all_applications())


@router.callback_query(ManagerCb(action=ManagerAction.all_applications).route)
@flags.del_from
async def handle_all_applications(query: CallbackQuery):
    applications = await Application.find(Application.is_checked == False).to_list()
    if len(applications) == 0:
        await query.answer('Заявок нет!', show_alert=True)
    for application in applications:
        await render_application_to_check(application, query.message)


@router.callback_query(ManagerCb(action=ManagerAction.verify_application).route)
async def handle_enter_id(query: CallbackQuery, state: FSMContext, callback_data: ManagerCb):
    application_id = callback_data.answer
    application = await Application.find_one(Application.id == int(application_id))
    try:
        if application.is_checked == True:
            await query.message.edit_caption(text=query.message.caption + '\nЗаявка согласована', reply_markup=None)
            return await query.answer('Заявка уже была согласована!', show_alert=True)
        await send_application_to_bitrix(application)
        #await notify_admins_and_managers(application, True)
        await bot.send_message(chat_id=application.user_id, text=f'Ваша заявка №{application_id} согласована')
        await application.set({'is_checked': True})
        await query.answer('Заявка успешно отправлена!', show_alert=True)
        await query.message.edit_caption(caption=query.message.caption + '\nЗаявка согласована', reply_markup=None)
    except Exception as e:
        logging.exception(e)
        await query.answer('Произошла ошибка!', show_alert=True)



@router.callback_query(ManagerCb(action=ManagerAction.block_application).route)
async def handle_enter_id(query: CallbackQuery, state: FSMContext, callback_data: ManagerCb):
    application_id = callback_data.answer
    application = await Application.find_one(Application.id == int(application_id))
    if application.is_checked == True:
        await query.message.edit_caption(caption=query.message.caption + '\nЗаявка отклонена', reply_markup=None)
        return await query.answer('Заявка уже была отклонена!', show_alert=True)
    await bot.send_message(chat_id=application.user_id, text=f'Ваша заявка №{application_id} не согласована')
    await application.set({'is_checked': True})
    #await notify_admins_and_managers(application, False)
    await query.message.edit_caption(caption=query.message.caption + '\nЗаявка отклонена',reply_markup=None)
