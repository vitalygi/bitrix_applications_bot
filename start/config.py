from os import getenv
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

admins = []
managers = []
admin_group =
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
