from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.create_application_fabric import *

choose_direction = ['Автопрокат', 'Стройка', 'УК Недвижимость',
                    'Маркетплейсы', 'ТЦ', 'Личное',
                    'Аренда недвижимости', 'Дивиденды ССС']

choose_payer = ['ООО "Мир Напитков"', 'ООО "Эволюция"', 'ООО "Фантом"',
                'ООО "Премьер"', 'ИП Сосновцев С.С.', 'ИП Сосновцева Н.В.',
                'ИП Соболева Т.В.', 'Другое']

choose_pay_form = ['наличная', 'безналичная', 'эл.деньги']


def create_application():
    """
    Создает клавиатуру для создания заявки.
    Не принимает параметров.
    Возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()
    create_cb = ApplicationCb(action=ApplicationAction.start_creation).pack()
    builder.button(text='Создать заявку', callback_data=create_cb)
    return builder.as_markup()


def choose_direction_kb():
    """
    Создает клавиатуру для выбора направления.
    Не принимает параметров.
    Возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()
    for text in choose_direction:
        cb = ApplicationCb(action=ApplicationAction.enter_direction, answer=text)
        builder.button(text=text, callback_data=cb)
    back_cb = ApplicationCb(action=ApplicationAction.start_creation)
    builder.button(text='Назад', callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()


def choose_pay_form_kb():
    """
    Создает клавиатуру для выбора формы оплаты.
    Не принимает параметров.
    Возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()
    for text in choose_pay_form:
        cb = ApplicationCb(action=ApplicationAction.enter_pay_form, answer=text)
        builder.button(text=text, callback_data=cb)
    back_cb = ApplicationCb(action=ApplicationAction.enter_responsible)
    builder.button(text='Назад', callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()


def choose_payer_kb():
    """
    Создает клавиатуру для выбора плательщика.
    Не принимает параметров.
    Возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()
    for text in choose_payer:
        cb = ApplicationCb(action=ApplicationAction.enter_payer, answer=text)
        builder.button(text=text, callback_data=cb)
    back_cb = ApplicationCb(action=ApplicationAction.enter_direction)
    builder.button(text='Назад', callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()


def choose_article_kb():
    """
    Создает клавиатуру для выбора статьи.
    Не принимает параметров.
    Возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()
    back_cb = ApplicationCb(action=ApplicationAction.enter_payer)
    builder.button(text='Назад', callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()


def send_application(application_id: int):
    """
    Отправляет заявку с указанным идентификатором.

    Принимает:
    application_id: int - идентификатор заявки.

    Возвращает:
    InlineKeyboardMarkup - клавиатура для отправки заявки.
    """
    builder = InlineKeyboardBuilder()
    cb = ApplicationCb(action=ApplicationAction.send_application, answer=str(application_id))
    back_cb = ApplicationCb(action=ApplicationAction.enter_file)
    builder.button(text='Отправить заявку',callback_data=cb)
    builder.button(text='Назад', callback_data=back_cb)
    builder.adjust(1)
    return builder.as_markup()
