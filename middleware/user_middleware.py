from typing import Dict, Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from data.models import User


class UserInjectionMiddleware(BaseMiddleware):
    """
    Middleware для инжекта юзеров
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        telegram_user = data["event_from_user"]
        telegram_id = int(telegram_user.id)
        first_name = telegram_user.first_name
        last_name = telegram_user.last_name
        if last_name:
            full_name = f"{first_name} {last_name}"
        else:
            full_name = first_name
        user: User = await User.find_one(User.id == telegram_id)
        if user is None:
            user = User(id=telegram_id,
                        nickname=full_name,
                        username=telegram_user.username)
        else:
            user.username = telegram_user.username
            user.nickname = full_name
        await user.save()
        data['user'] = user
        # inject any data to event
        event = event.model_copy(update={"is_registered": True if user is not None and user.is_registered == True else False,
                                         "name": user.name})

        return await handler(event, data)
