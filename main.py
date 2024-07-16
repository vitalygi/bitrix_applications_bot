# загрузка переменных по всему коду
import start.load_env
import asyncio
import logging
import sys
from start.bot import start




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
