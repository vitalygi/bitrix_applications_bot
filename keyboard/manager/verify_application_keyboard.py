from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.manager_fabric import *


def all_applications():
    """
    Функция создает клавиатуру для всех заявок.
    Не принимает параметров.
    Возвращает клавиатуру в виде разметки.
    """
    builder = InlineKeyboardBuilder()
    all_applications_cb = ManagerCb(action=ManagerAction.all_applications).pack()
    builder.button(text='Мои заявки', callback_data=all_applications_cb)
    return builder.as_markup()


def verify_application_kb(application_id):
    """
    Функция создает клавиатуру для подтверждения или отклонения заявки.
    Принимает идентификатор заявки в качестве параметра.
    Возвращает клавиатуру в виде разметки.
    """
    builder = InlineKeyboardBuilder()
    verify_cb = ManagerCb(action=ManagerAction.verify_application, answer=str(application_id))
    block_cb = ManagerCb(action=ManagerAction.block_application, answer=str(application_id))
    builder.button(text='Согласовать', callback_data=verify_cb)
    builder.button(text='Отказать', callback_data=block_cb)
    builder.adjust(1)
    return builder.as_markup()
