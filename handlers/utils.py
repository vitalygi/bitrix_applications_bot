from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from start.config import bot


async def change_state_key(state: FSMContext, key, value):
    data = await state.get_data()
    data[key] = value
    await state.set_data(data)


async def change_user_state_data_key(dispatcher, user_id, key, value):
    storage_key = StorageKey(
        chat_id=user_id,
        user_id=user_id,
        bot_id=bot.id)
    data = await dispatcher.fsm.storage.get_data(key=storage_key)
    data[key] = value
    await dispatcher.fsm.storage.set_data(key=storage_key, data=data)
