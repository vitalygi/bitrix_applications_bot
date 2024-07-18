from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.verification_user_fabric import *

from data.models import User


def user_verification_kb(user: User, adjust: int = 1):
    """
    Функция создает клавиатуру для верификации пользователя.

    Параметры:
    - user: User - объект пользователя, который требует верификации.
    - adjust: int - значение для настройки клавиатуры (по умолчанию 1).

    Возвращает:
    - InlineKeyboardMarkup: клавиатура верификации пользователя в виде разметки.
    """
    builder = InlineKeyboardBuilder()
    verify_cb = VerificationCb(action=VerificationAction.verify_user, user_id=user.id)
    block_cb = VerificationCb(action=VerificationAction.block_user, user_id=user.id)
    builder.button(text='Активировать', callback_data=verify_cb)
    builder.button(text='Заблокировать', callback_data=block_cb)
    builder.adjust(adjust)
    return builder.as_markup()


