from aiogram.types import Message

from data.models import Application, User
from keyboard.manager.verify_application_keyboard import verify_application_kb


async def render_application_to_check(application: Application, message: Message):
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
Ответственный:{application.responsible}
Направление:{application.direction}
Форма оплаты:{application.pay_form}
Плательщик:{application.payer}
Статья:{application.article}
Комментарии:{application.comments}
Сумма:{application.amount}
Дата оплаты:{application.payment_date}
Доп.информация для оплаты:{application.add_info}
"""
    keyboard = verify_application_kb(application.id)
    if application.file_type == 'document':
        await message.answer_document(caption=text, document=application.file, reply_markup=keyboard)
    else:
        await message.answer_photo(caption=text, photo=application.file, reply_markup=keyboard)



