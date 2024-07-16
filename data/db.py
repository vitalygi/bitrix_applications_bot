import logging
from os import getenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from .models import *

URI = getenv('DATABASE_URI')


class Database:

    @classmethod
    async def init(cls):
        """
            Init motor + beanie
        :return:
        """
        client = AsyncIOMotorClient(URI)
        await init_beanie(database=client.cbd, document_models=[Product])
        logging.log(level=logging.INFO, msg='Database started')
