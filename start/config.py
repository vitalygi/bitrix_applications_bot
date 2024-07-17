from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


admins = [450626281]
managers = [450626281]
admin_group = -1002245837205
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
