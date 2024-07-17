import logging.config

from .config import bot
from handlers.register import register_dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
import yaml


with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)


async def start():
    dp = await register_dispatcher(storage=RedisStorage(Redis()))#host='redis')))
    await dp.start_polling(bot)
