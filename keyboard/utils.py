from aiogram.utils.keyboard import InlineKeyboardBuilder

from routers.create_application_fabric import ApplicationCb,ApplicationAction


def application_back_markup_with_action(action: ApplicationAction,button_text='Назад'):
    """
    Функция создает разметку кнопки "Назад" для приложения с заданным действием и текстом кнопки.
    """
    builder = InlineKeyboardBuilder()
    cb = ApplicationCb(action=action)
    builder.button(text=button_text,callback_data=cb)
    return builder.as_markup()