from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.admin_fabric import *

from data.models import User


def main_menu(adjust: int = 1):
    """
    Генерирует основное меню с кнопками для всех пользователей и ввода ID.

    :param adjust: int, опциональный параметр для настройки меню
    :return: InlineKeyboardMarkup, сгенерированное меню в виде разметки
    """
    builder = InlineKeyboardBuilder()
    all_users_cb = AdminCb(action=AdminAction.all_users)
    enter_id_cb = AdminCb(action=AdminAction.enter_id)
    builder.button(text='Пользователи', callback_data=all_users_cb)
    builder.button(text='Ввести ID', callback_data=enter_id_cb)
    builder.adjust(adjust)
    return builder.as_markup()

def back_menu(adjust: int = 1):
    """
    Генерирует меню "Вернуться в меню" с возможностью настройки.

    :param adjust: int, опциональный параметр для настройки меню
    :return: InlineKeyboardMarkup, сгенерированное меню "Вернуться в меню" в виде разметки
    """
    builder = InlineKeyboardBuilder()
    menu = AdminCb(action=AdminAction.menu)
    builder.button(text='В меню', callback_data=menu)
    builder.adjust(adjust)
    return builder.as_markup()


