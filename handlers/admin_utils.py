from data.models import User
from start.config import admin_group
from start.config import bot
from keyboard.admin.verify_keyboard import user_verification_kb
from static.admin.verify_user import verify_user


async def send_register_user_application_to_group(user: User):
    kb = user_verification_kb(user)
    await bot.send_message(
        chat_id=admin_group,
        text=verify_user(user),
        reply_markup=kb)
