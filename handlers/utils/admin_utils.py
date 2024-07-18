from typing import List

from data.models import User
from start.config import admin_group
from start.config import bot
from keyboard.admin.verify_keyboard import user_verification_kb
from static.admin.verify_user import verify_user
import pandas as pd


async def send_register_user_application_to_group(user: User):
    """
    Отправляет заявку на регистрацию пользователя в группу.

    :param user: Пользователь, для которого отправляется заявка.
    :type user: User

    :return: Нет возвращаемого значения.
    """
    kb = user_verification_kb(user)
    await bot.send_message(
        chat_id=admin_group,
        text=verify_user(user),
        reply_markup=kb)


def structure_to_xlsx(active_users, banned_users, file_path='users.xlsx'):
    """
    Функция для структурирования данных пользователей в Excel файл.

    :param active_users: Список активных пользователей.
    :param banned_users: Список заблокированных пользователей.
    :param file_path: Путь к файлу Excel (по умолчанию 'users.xlsx').
    :type active_users: list
    :type banned_users: list
    :type file_path: str

    :return: Нет возвращаемого значения.
    """
    active_df = pd.DataFrame(active_users)
    banned_df = pd.DataFrame(banned_users)

    writer = pd.ExcelWriter(file_path)
    active_df.to_excel(writer, 'Активные пользователи', index=False, header=False, na_rep='')
    for column in active_df:
        column_width = 20
        col_idx = active_df.columns.get_loc(column)
        writer.sheets['Активные пользователи'].set_column(col_idx, col_idx, column_width)

    banned_df.to_excel(writer, 'Заблокированные пользователи', index=False, header=False, na_rep='')
    for column in active_df:
        column_width = 20
        col_idx = active_df.columns.get_loc(column)
        writer.sheets['Заблокированные пользователи'].set_column(col_idx, col_idx, column_width)

    writer.close()


def save_users_to_file(users: List[User]):
    """
    Функция для сохранения пользователей в файл Excel.

    :param users: Список пользователей для сохранения.
    :type users: List[User]

    :return: Нет возвращаемого значения.
    """
    active_users = [['ID', 'ФИО', 'Статус', 'Дата регистрации']]
    banned_users = [['ID', 'ФИО', 'Статус', 'Дата регистрации']]
    for user in users:
        if user.name is not None and len(user.name) != 0 and user.name != '':
            if user.is_registered:
                register_info = 'Активен'
                active_users.append([user.id, user.name, register_info, user.register_date])
            else:
                register_info = 'Не активен'
                banned_users.append([user.id, user.name, register_info, user.register_date])
    structure_to_xlsx(active_users, banned_users, 'users.xlsx')
