from .config import bot
from handlers.register import register_dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


async def start():
    dp = await register_dispatcher(storage=RedisStorage(Redis(host='redis')))
    await dp.start_polling(bot)
