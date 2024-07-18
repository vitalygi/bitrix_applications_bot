import random

from aiogram import Router, flags
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from data.models import Application, User
from filters.register_filter import IsRegistered
from handlers.user.widgets.calendar import CalendarState, calendar_dialog
from handlers.utils.utils import mark_message_to_del
from keyboard.user.application_keyboard import *
from keyboard.utils import application_back_markup_with_action
from routers.create_application_fabric import *
from handlers.utils.utils import change_state_key
from states.user.create_application import ApplicationStatesGroup
from keyboard.user.application_keyboard import create_application as create_application_kb

router = Router()

router.message.filter(IsRegistered())
router.callback_query.filter(IsRegistered())

router.include_routers(calendar_dialog)


@router.callback_query(ApplicationCb(action=ApplicationAction.start_creation).route)
@flags.del_from
async def start_application_creation(query: CallbackQuery, state: FSMContext):
    await mark_message_to_del(await query.message.answer('Введите ответственного:'), state)
    await state.set_state(ApplicationStatesGroup.enter_responsible)


@router.message(ApplicationStatesGroup.enter_responsible)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_responsible).route)
@flags.del_from
async def enter_responsible_handler(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        await change_state_key(state, 'responsible', message.text)
    else:
        message = message.message
    await message.answer(text='Выберите направление:', reply_markup=choose_direction_kb())


@router.callback_query(ApplicationCb(action=ApplicationAction.enter_direction).route)
@flags.del_from
async def enter_direction(query: CallbackQuery, callback_data: ApplicationCb, state: FSMContext):
    if callback_data.answer is not None:
        await change_state_key(state, 'direction', callback_data.answer)
    await query.message.answer(text='Форма оплаты:', reply_markup=choose_pay_form_kb())


@router.callback_query(ApplicationCb(action=ApplicationAction.enter_pay_form).route)
@flags.del_from
async def enter_direction(query: CallbackQuery, callback_data: ApplicationCb, state: FSMContext):
    if callback_data.answer is not None:
        await change_state_key(state, 'pay_form', callback_data.answer)
    await query.message.answer(text='Плательщик:', reply_markup=choose_payer_kb())


@router.callback_query(ApplicationCb(action=ApplicationAction.enter_payer).route)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_article).route)
@flags.del_from
async def enter_direction(query: CallbackQuery, callback_data: ApplicationCb, state: FSMContext):
    if callback_data.answer is not None:
        await change_state_key(state, 'payer', callback_data.answer)
    await mark_message_to_del(await query.message.answer('Введите статью:',
                                                         reply_markup=application_back_markup_with_action(
                                                             ApplicationAction.enter_pay_form)), state)
    await state.set_state(ApplicationStatesGroup.enter_article)


@router.message(ApplicationStatesGroup.enter_article)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_comments).route)
@flags.del_from
async def enter_responsible_handler(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        await change_state_key(state, 'article', message.text)
    else:
        message = message.message
    await mark_message_to_del(await message.answer('Введите комментарии:',
                                                   reply_markup=application_back_markup_with_action(
                                                       ApplicationAction.enter_article)), state)
    await state.set_state(ApplicationStatesGroup.enter_comments)


@router.message(ApplicationStatesGroup.enter_comments)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_amount).route)
@flags.del_from
async def enter_comments(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        await change_state_key(state, 'comments', message.text)
    else:
        message = message.message
    await mark_message_to_del(await message.answer('Введите сумму:',
                                                   reply_markup=application_back_markup_with_action(
                                                       ApplicationAction.enter_comments)), state)
    await state.set_state(ApplicationStatesGroup.enter_amount)


@router.message(ApplicationStatesGroup.enter_amount)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_payment_date).route)
@flags.del_from
async def enter_responsible_handler(message: Message, state: FSMContext, dialog_manager: DialogManager):
    if not isinstance(message, CallbackQuery):
        try:
            int(message.text)
            await change_state_key(state, 'amount', message.text)
        except:
            await state.set_state(ApplicationStatesGroup.enter_amount)
            return await mark_message_to_del(await message.answer('Вы ввели не число, попробуйте ещё раз\nВведите сумму:',
                                                   reply_markup=application_back_markup_with_action(
                                                       ApplicationAction.enter_comments)), state)
    await dialog_manager.start(CalendarState.MAIN, mode=StartMode.RESET_STACK)
    await state.set_state(CalendarState.MAIN)


@router.callback_query(ApplicationCb(action=ApplicationAction.enter_add_info).route)
@flags.del_from
async def enter_responsible_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(ApplicationStatesGroup.enter_add_info)
    await mark_message_to_del(await query.message.answer('Доп.информация для оплаты:',
                                                         reply_markup=application_back_markup_with_action(
                                                             ApplicationAction.enter_payment_date)), state)


@router.message(ApplicationStatesGroup.enter_add_info)
@router.message(ApplicationStatesGroup.enter_file, F.text)
@router.callback_query(ApplicationCb(action=ApplicationAction.enter_file).route)
@flags.del_from
async def enter_responsible_handler(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        await change_state_key(state, 'add_info', message.text)
    else:
        message = message.message
    await mark_message_to_del(await message.answer('Прикрепить документ,фото',
                                                   reply_markup=application_back_markup_with_action(
                                                       ApplicationAction.enter_add_info)), state)
    await state.set_state(ApplicationStatesGroup.enter_file)


@router.message(ApplicationStatesGroup.enter_file, F.photo)
@router.message(ApplicationStatesGroup.enter_file, F.document)
@router.callback_query(ApplicationCb(action=ApplicationAction.check_application).route)
@flags.del_from
async def enter_responsible_handler(message: Message, state: FSMContext):
    if not isinstance(message, CallbackQuery):
        file = message.document if message.document is not None else message.photo[-1]
        file_type = 'document' if message.document is not None else 'photo'
        file_id = file.file_id
        await change_state_key(state, 'file', file_id)
        await change_state_key(state, 'file_type', file_type)
    else:
        message = message.message

    application_id = random.randint(1, 1_000_000_000)

    await message.answer(f'Заявка №{application_id} готова\nНажмите кнопку Отправить заявку',
                         reply_markup=send_application(application_id))
    await state.set_state(None)


@router.callback_query(ApplicationCb(action=ApplicationAction.send_application).route)
@flags.del_from
async def enter_responsible_handler(query: CallbackQuery, callback_data: ApplicationCb, state: FSMContext, user: User):
    application = await create_application(callback_data.answer, state, user.id)
    caption = f'Ваша заявка №{application.id} передана на рассмотрение'
    if application.file_type == 'document':
        await query.message.answer_document(document=application.file, caption=caption)
    else:
        await query.message.answer_photo(photo=application.file, caption=caption)
    await application.save()
    await query.message.answer(text='Создать заявку', reply_markup=create_application_kb())
    await state.set_state(None)


async def create_application(application_id, state: FSMContext, user_id) -> Application:
    data = await state.get_data()
    responsible = data.get('responsible', '')
    direction = data.get('direction', '')
    pay_form = data.get('pay_form', '')
    payer = data.get('payer', '')
    article = data.get('article', '')
    comments = data.get('comments', '')
    amount = data.get('amount', 0)
    payment_date = data.get('payment_date', '')
    add_info = data.get('add_info', '')
    file = data.get('file', '')
    file_type = data.get('file_type', '')
    application = Application(
        id=int(application_id),
        user_id=user_id,
        responsible=responsible,
        direction=direction,
        pay_form=pay_form,
        payer=payer,
        article=article,
        comments=comments,
        amount=amount,
        payment_date=payment_date,
        add_info=add_info,
        file=file,
        file_type=file_type)
    return application
