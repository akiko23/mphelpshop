from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from db import Database


BOT_TOKEN = os.environ.get("BOT_TOKEN")
DB_FILE = 'db.sqlite3'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database(DB_FILE)

secretKey = os.environ.get('SECRET_KEY').encode('utf-8')

