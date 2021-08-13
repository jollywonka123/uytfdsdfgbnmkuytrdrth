from aiogram import Bot, Dispatcher, executor
import asyncio
from config import token
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

db1 = sqlite3.connect('users.db', check_same_thread = False)
db2 = sqlite3.connect('zayavka.db', check_same_thread = False)
db3 = sqlite3.connect('pay.db', check_same_thread = False)

sql1 = db1.cursor()
sql2 = db2.cursor()
sql3 = db3.cursor()

sql1.execute("""CREATE TABLE IF NOT EXISTS users(
    chatid INT,
    username TEXT,
    status INT,
    zalet INT,
    percent INT
)""")
db1.commit()

sql2.execute("""CREATE TABLE IF NOT EXISTS zayavka(
    chatid INT,
    username TEXT,
    reffer TEXT,
    lolz TEXT,
    time TEXT,
    opit TEXT
)""")
db2.commit()

sql3.execute("""CREATE TABLE IF NOT EXISTS pay(
    service TEXT,
    payment_details TEXT,
    info TEXT
)""")

if __name__ == '__main__':
    from handlers import dp, on_startup
    executor.start_polling(dp, on_startup=on_startup)
