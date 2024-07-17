from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.create_application_fabric import *

choose_direction = ['Автопрокат', 'Стройка', 'УК Недвижимость',
                    'Маркетплейсы', 'ТЦ', 'Личное',
                    'Аренда недвижимости', 'Дивиденды ССС']

choose_payer = ['ООО "Мир Напитков"', 'ООО "Эволюция"', 'ООО "Фантом"',
                'ООО "Премьер"', 'ИП Сосновцев С.С.', 'ИП Сосновцева Н.В.',
                'ИП Соболева Т.В.', 'Другое']


def create_application():
    builder = InlineKeyboardBuilder()
    create_cb = ApplicationCb(action=ApplicationAction.start_creation).pack()
    builder.button(text='Создать заявку', callback_data=create_cb)
    return builder.as_markup()


def choose_direction_kb():
    builder = InlineKeyboardBuilder()
    for text in choose_direction:
        cb = ApplicationCb(action=ApplicationAction.enter_direction, answer=text)
        builder.button(text=text, callback_data=cb)
    back_cb = ApplicationCb(action=ApplicationAction.back,answer='enter_responsible')
    builder.button(text='Назад',callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()
