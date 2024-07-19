import logging.config

from aiogram.fsm.storage.base import DefaultKeyBuilder

from .config import bot
from handlers.register import register_dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
import yaml

from os import getenv

with open("logging.yaml", "r") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)
START_TYPE = getenv("START_TYPE")
redis_host = 'redis' if START_TYPE != 'DEBUG' else 'localhost'

async def start():
    dp = await register_dispatcher(storage=RedisStorage(Redis(host=redis_host),key_builder=DefaultKeyBuilder(with_destiny=True)))
    await dp.start_polling(bot)
