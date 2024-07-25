from contextlib import suppress

from aiogram.types import Message

from data.models import Application, User
from keyboard.manager.verify_application_keyboard import verify_application_kb
from start.config import managers, bot
from keyboard.manager.verify_application_keyboard import all_applications


async def render_application_to_check(application: Application, message: Message = None, manager_id: int = None):
    """
    Рендерит информацию о заявке для проверки и отправляет ее в виде документа или фотографии в зависимости от типа файла.

    Параметры:
        - application: Application - объект заявки
        - message: Message - сообщение, в которое будет отправлена информация

    Возвращаемые значения:
        - Нет (async function)
    """
    user: User = await User.find_one(User.id == application.user_id)
    text = f"""
Заявка №{application.id} от {user.name}
Ответственный: {application.responsible}
Направление: {application.direction}
Форма оплаты: {application.pay_form}
Плательщик: {application.payer}
Статья: {application.article}
Комментарии: {application.comments}
Сумма: {application.amount}
Дата оплаты: {application.payment_date}
Доп.информация для оплаты: {application.add_info}
Дата создания: {application.date}
"""
    keyboard = verify_application_kb(application.id)
    if application.file_type == 'document':
        if message == None:
            return await bot.send_document(chat_id=manager_id, caption=text, document=application.file,
                                           reply_markup=keyboard)
        await message.answer_document(caption=text, document=application.file, reply_markup=keyboard)
    else:
        if message == None:
            return await bot.send_photo(chat_id=manager_id, caption=text, photo=application.file, reply_markup=keyboard)
        await message.answer_photo(caption=text, photo=application.file, reply_markup=keyboard)


async def notify_managers(application: Application):
    """
    Функция уведомляет менеджеров о новой заявке.

    :param application: Объект заявки
    """
    to_mail = [*managers]
    ids_to_send = set(to_mail)
    for id in ids_to_send:
        with suppress(Exception):
            await render_application_to_check(application, manager_id=id)
