import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

from .config import configuration
from .subscribers import Subscribers
from .scheduler import SchedulerMessage

bot = Bot(token=configuration.bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
subscribers = Subscribers(configuration.subscribers_file_path)

async def startup(dispatcher: Dispatcher):
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


def start_bot():
    log_folder_path = os.path.abspath(configuration.log_folder_path)
    log_file_path = os.path.join(log_folder_path, "bot.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=logging.INFO, filename=log_file_path, format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")
    logging.info(f"Bot started. Log file {log_file_path}")

    scheduler_message = SchedulerMessage(bot, subscribers)
    scheduler_message.add_event(hour=11, minutes=0)
    scheduler_message.add_event(hour=15, minutes=0)
    scheduler_message.add_event(hour=20, minutes=0)

    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
