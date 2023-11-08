import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .config import configuration
from .log_factory import creating_log
from .subscribers import Subscribers
from .scheduler import SchedulerMessage
from .messages_builder import MessagesBuilder
from .red_alert import red_alert_checking
from .KidnappedPerson import KidnappedPerson

creating_log()

# Define user states
class UserStatus(StatesGroup):
    MAIN_MENU = State()  # Main menu state

bot = Bot(token=configuration.bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
subscribers = Subscribers(configuration.subscribers_file_path)
messages_builder = MessagesBuilder(configuration.data_folder_path)
kidnapped_person = KidnappedPerson(configuration.kidnapped_person_file_path,  configuration.log_folder_path)


async def startup(dispatcher: Dispatcher):
    None

async def shutdown(dispatcher: Dispatcher):
    await storage.close()
    await bot.close()

def message_log(message, custom=""):
    user = message['from']
    logging.info(f"{custom}Message from {user.id} ({user.first_name}, {user.username}): {message.text}")

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/test"))
    keyboard.add(KeyboardButton("/kidnapped"))
    # keyboard.add(KeyboardButton("/calendar"))
    # keyboard.add(KeyboardButton("/weather"))
    # keyboard.add(KeyboardButton("/forecast"))
    # keyboard.add(KeyboardButton("/beaches"))
    # keyboard.add(KeyboardButton("/gematria"))
    return keyboard


async def send_random_photo(chat_id):
    random_file = kidnapped_person.get_random()
    with open(random_file, "rb") as photo_file:
        await bot.send_photo(chat_id, photo_file, caption="#brinbthemhome #KidnappedFromIsrael")

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message, state: FSMContext):
    message_log(message, "[start_command] ")
    await state.finish()  # Clear any existing state
    await UserStatus.MAIN_MENU.set()  # Set the user state to main menu
    await message.reply("Hi, Select command from menu", reply_markup=get_main_menu())

@dp.message_handler(state=UserStatus.MAIN_MENU)
async def process_message(message: types.Message, state: FSMContext):
    subscribers.add_chat_id(message.chat.id)
    message_log(message, custom="[process_message] ")
    if message.text == "/start":
        await start_command(message, state)
    elif message.text == "/test":
        await message.reply(messages_builder.get_tehilim_message())
        await message.reply(messages_builder.get_oref_message())
        await message.reply(messages_builder.get_truma_message())
        await message.reply(messages_builder.get_message("tfila_message.txt"))
        await message.reply(messages_builder.get_daily_message())
    elif message.text == "/kidnapped":
        await send_random_photo(message.chat.id)
        # random_file = kidnapped_person.get_random()
        # with open(random_file, "rb") as photo_file:
        #     await message.bot.send_photo(message.chat.id, photo_file, caption="Kidnapped Person")
    else:
        await message.reply(f"echo '{message}'")


def start_bot():
    n = kidnapped_person.get_total_pages_number()
    logging.info(f"Total pages number: {n}")

    scheduler_message = SchedulerMessage(bot, subscribers)

    all_items = messages_builder.import_scheduler()
    for hour, minutes, message_file_name in all_items:
        message_func = lambda m=message_file_name: messages_builder.get_message(m)
        scheduler_message.add_event(hour=hour, minutes=minutes, message_func=message_func)
    scheduler_message.add_event(hour=9, minutes=0, message_func=messages_builder.get_daily_message)
    scheduler_message.add_custom_event(hour=20, minutes=30, custom_event=send_random_photo)
    # scheduler_message.add_polling(custom_polling_func=red_alert_checking, sleep_seconds=1)

    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
