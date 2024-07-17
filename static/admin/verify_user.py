from data.models import User


def verify_user(user: User):
    return f"""
ФИО: {user.name}
ID:{user.id}
"""
