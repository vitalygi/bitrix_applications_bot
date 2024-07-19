from data.models import User


def verify_user(user: User):
    """
    Функция верификации пользователя. Принимает объект пользователя типа User.
    Возвращает строку с ФИО пользователя и его ID.
    """
    return f"""
ФИО: {user.name}
ID:{user.id}
"""
