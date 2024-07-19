import base64
import io
import logging
from os import getenv

from start.config import bot
import aiohttp
from data.models import Application, User

BITRIX24_WEBHOOK_URL = getenv('BITRIX24_WEBHOOK_URL')


async def send_application_to_bitrix(application: Application):
    """
    Функция отправляет заявку в Bitrix.

    args:
        application (Application): Заявка, которую необходимо отправить.

    Returns:
        None
    """
    user: User = await User.find_one(User.id == application.user_id)
    deal_id = await create_bitrix24_deal(application, user)
    file_name, file_base64 = await file_to_base64(application.file)
    await attach_file_to_deal(deal_id, file_name, file_base64)


async def file_to_base64(file_id) -> [str, str]:
    """
    Преобразует файл в формат base64.

    Args:
        file_id: идентификатор файла, который необходимо преобразовать.

    Returns:
        Кортеж с именем файла и строкой base64.
    """
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = file_path[file_path.find('/') + 1:]
    file_io = io.BytesIO()
    await bot.download_file(file_path, file_io)
    file_bytes = file_io.getvalue()
    file_64_encode = base64.b64encode(file_bytes)
    base64_string = file_64_encode.decode('utf-8')
    return file_name, base64_string


async def create_bitrix24_deal(application: Application, user: User):
    """
    Функция создает сделку в Bitrix24 на основе данных заявки и пользователя.

    Args:
        application (Application): Объект заявки.
        user (User): Объект пользователя.

    Returns:
        Результат создания сделки в Bitrix24.
    """

    payload = {
        'fields': {
            "UF_CRM_CHAT_ID": application.id,
            "UF_CRM_USER_ID": application.user_id,
            "UF_CRM_1652262143654": user.name,
            "UF_CRM_1720962682790": application.direction,
            "UF_CRM_1657703623063": application.pay_form,
            "UF_CRM_1720962991461": application.payer,
            "STAGE_ID": "C215:NEW",
            "UF_CRM_1720963068746": application.article,
            "COMMENTS": application.comments,
            "OPPORTUNITY": application.amount,
            "CURRENCY_ID": "RUB",
            "UF_CRM_1720963303158": application.payment_date,
            "UF_CRM_1720963364889": application.add_info,
            "CATEGORY_ID": 215
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BITRIX24_WEBHOOK_URL}/crm.deal.add.json", json=payload) as resp:
            if resp.status == 200:
                answer = await resp.json()
                logging.info(f'Заявка №{application.id}  создана', answer)
                return answer.get('result')
    return None


async def attach_file_to_deal(deal_id, file_name, file_base64):
    """
    Функция прикрепляет файл к сделке в Bitrix24.

    Args:
        deal_id: идентификатор сделки.
        file_name: имя файла.
        file_base64: файл в формате base64.

    Returns:
        None
    """
    payload = {
        'id': deal_id,
        'fields': {
            'UF_CRM_1628766324157': {
                'fileData': [
                    file_name,
                    file_base64,
                ],
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        await session.post(f"{BITRIX24_WEBHOOK_URL}/crm.deal.update.json", json=payload)
        logging.info(f'Файл {file_name} к заявке {deal_id} прикреплен')
