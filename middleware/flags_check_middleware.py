from typing import Dict, Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import TelegramObject, Message


class CheckFlagsMiddleware(BaseMiddleware):
    """
    Middleware для проверки флагов
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        message = event if isinstance(event, Message) else event.message
        del_from = get_flag(data, "del_from")
        if not del_from:
            return await handler(event, data)
        else:
            try:
                await message.delete()
            except:
                pass
            return await handler(event, data)
