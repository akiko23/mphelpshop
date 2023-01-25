from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from db import Database


BOT_TOKEN = "5875663139:AAFACUhFV5bNoUel6C1E7KbdUP2GFlTkyI4"
DB_FILE = 'db.sqlite3'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
db = Database(DB_FILE)

secretKey = '5ad8d388d4fbf52d6c4e539d6b3248a0'.encode('utf-8')

