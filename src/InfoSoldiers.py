import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

from .config import configuration

bot = Bot(token=configuration.bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
    message_log(message, custom="[process_message] ")
    await message.reply(f"echo '{message}'")


def start_bot():
    log_folder_path = configuration.log_folder_path
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.basicConfig(level=logging.INFO, filename=os.path.join(log_folder_path, "bot.log"), format="%(asctime)s - %(levelname)s - %(message)s")
    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
