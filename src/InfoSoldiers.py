import os
from datetime import datetime, timedelta
import logging
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

from .config import configuration
from .subscribers import Subscribers

bot = Bot(token=configuration.bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
subscribers = Subscribers(configuration.subscribers_file_path)

async def startup(dispatcher: Dispatcher):
    # await bot.send_message(configuration.chat_id=369737554, text='Hello', reply_markup=get_main_menu())
    # await state.finish()  # Clear any existing state
    # await UserStatus.MAIN_MENU.set()  # Set the user state to main menu
    None

async def shutdown(dispatcher: Dispatcher):
    await storage.close()
    await bot.close()

def message_log(message, custom=""):
    user = message['from']
    logging.info(f"{custom}Message from {user.id} ({user.first_name}, {user.username}): {message.text}")

@dp.message_handler()
async def process_message(message: types.Message, state: FSMContext):
    subscribers.add_chat_id(message.chat.id)
    message_log(message, custom="[process_message] ")
    await message.reply(f"echo '{message}'")

# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     logging.info(f"start {message.chat.id}")
#     # Add the user to the list of subscribers
#     subscribers.add(message.chat.id)
#     await message.reply("You are now subscribed to receive messages.")

async def send_scheduled_message():
    message = 'שלום לכולם! למי שמעוניין בדרך חוץ מכסף לתמוך בחיילים החטופים ובעם ישראל, מומלץ לקרוא פרקי תהילים במלחמה לשם ביטחון. \
תהילים פרק קכ"א  \
[https://tehilim.co/chapter/121/] \
תהילים פרק ק"ל \
[https://tehilim.co/chapter/130/] \
המשך יום טוב .👋'
    while True:
        now = datetime.now()
        target_time = now.replace(hour=10, minute=00, second=0, microsecond=0)
        time_until_target = target_time - now
        if time_until_target.total_seconds() < 0:
            target_time += timedelta(days=1)
        await asyncio.sleep((target_time - datetime.now()).total_seconds())
        for chat_id in subscribers.get_all():
            await bot.send_message(chat_id=chat_id, text=message)
        logging.info("Scheduled message sent.")

def start_bot():
    log_folder_path = os.path.abspath(configuration.log_folder_path)
    log_file_path = os.path.join(log_folder_path, "bot.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    # logging.basicConfig(level=logging.INFO, filename=log_file_path, format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")
    logging.info(f"Bot started. Log file {log_file_path}")

    loop = asyncio.get_event_loop()
    loop.create_task(send_scheduled_message())

    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
