from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
TOKEN = "**********************************************"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
   executor.start_polling(dp)
