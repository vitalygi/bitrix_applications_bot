from contextlib import suppress

import pymongo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import Message

from keyboard.admin.verify_keyboard import user_verification_kb
from start.config import admins, managers, admin_group
from data.models import Application, User
from start.config import bot


async def change_state_key(state: FSMContext, key, value):
    """
    Функция изменяет ключ состояния на указанное значение.

    :param state: Контекст конечного автомата, содержащий данные состояния
    :param key: Ключ, который нужно изменить
    :param value: Новое значение ключа
    """
    data = await state.get_data()
    data[key] = value
    await state.set_data(data)


async def mark_message_to_del(message: Message, state: FSMContext):
    """
    Функция отмечает сообщение для удаления из состояния FSM.

    :param message: Сообщение, которое нужно отметить для удаления
    :param state: Контекст конечного автомата, содержащий данные состояния
    """
    data = await state.get_data()
    messages_to_del = data.get('messages_to_del', [])
    messages_to_del.append(message.message_id)
    data['messages_to_del'] = messages_to_del
    await state.set_data(data=data)


async def change_user_state_data_key(dispatcher, user_id, key, value):
    """
    Функция изменяет ключ состояния пользователя на указанное значение.

    :param dispatcher: Диспетчер для работы с хранилищем данных
    :param user_id: Идентификатор пользователя
    :param key: Ключ, который нужно изменить
    :param value: Новое значение ключа
    """
    storage_key = StorageKey(
        chat_id=user_id,
        user_id=user_id,
        bot_id=bot.id)
    data = await dispatcher.fsm.storage.get_data(key=storage_key)
    data[key] = value
    await dispatcher.fsm.storage.set_data(key=storage_key, data=data)


async def notify_admins_and_managers(application: Application, status: bool):
    """
    Функция уведомляет администраторов и менеджеров о заявке, отправляя сообщение с информацией о заявке и статусе.

    :param application: Объект заявки
    :param status: Статус заявки (True - согласована, False - не согласована)
    """
    to_mail = [*admins, *managers]
    ids_to_send = set(to_mail)
    for id in ids_to_send:
        user: User = await User.find_one(User.id == application.user_id)
        text = f"""
Заявка №{application.id} от {user.name} {'согласована' if status else 'не согласована'}
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
        with suppress(Exception):
            if application.file_type == 'document':
                await bot.send_document(chat_id=id, caption=text, document=application.file)
            else:
                await bot.send_photo(chat_id=id, caption=text, photo=application.file)


async def get_application_id() -> int:
    """
    Функция возвращает уникальный идентификатор заявки.

    :return: Уникальный идентификатор заявки
    """
    last_application = await Application.find().sort("id").to_list()
    return last_application[-1].id + 1 if last_application and len(last_application) > 0 else 1
