import contextlib
import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.utils.utils import change_state_key, mark_message_to_del
from keyboard.utils import application_back_markup_with_action
from routers.create_application_fabric import ApplicationAction
from states.user.create_application import ApplicationStatesGroup


async def date_selected(query: CallbackQuery, state: FSMContext,
                        selected_date: str):
    """
        Отправка сообщения после выбора даты в календаре
    """
    with contextlib.suppress(Exception):
        await query.message.delete()
    selected_date = datetime.datetime.fromisoformat(selected_date).strftime('%d.%m.%Y')
    await change_state_key(state, 'payment_date', selected_date)
    await state.set_state(ApplicationStatesGroup.enter_add_info)
    await mark_message_to_del(await query.message.answer('Доп.информация для оплаты:',
                                                         reply_markup=application_back_markup_with_action(
                                                             ApplicationAction.enter_payment_date)), state)
