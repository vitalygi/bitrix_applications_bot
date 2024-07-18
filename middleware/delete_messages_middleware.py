from typing import Dict, Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DeleteMessagesMiddleware(BaseMiddleware):
    """
    Middleware для удаления сообщений из state[messages_to_del]
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        state = data['state']
        state_data = await state.get_data()
        messages_to_del = state_data.get('messages_to_del', [])
        telegram_user = data["event_from_user"]
        telegram_id = telegram_user.id
        if len(messages_to_del) > 0:
            try:
                await event.bot.delete_messages(chat_id=telegram_id, message_ids=messages_to_del)
            except Exception as e:
                pass
            state_data['messages_to_del'] = []
            await state.set_data(state_data)
        return await handler(event, data)
