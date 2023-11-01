import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext

from .config import configuration
from .log_factory import creating_log
from .subscribers import Subscribers
from .scheduler import SchedulerMessage
from .messages_builder import MessagesBuilder
from .red_alert import red_alert_checking

creating_log()

bot = Bot(token=configuration.bot_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
subscribers = Subscribers(configuration.subscribers_file_path)
messages_builder = MessagesBuilder(configuration.data_folder_path)


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
    if message.text == "/test":
        await message.reply(messages_builder.get_tehilim_message())
        await message.reply(messages_builder.get_oref_message())
        await message.reply(messages_builder.get_truma_message())
        await message.reply(messages_builder.get_message("tfila_message.txt"))
        await message.reply(messages_builder.get_daily_message())
    else:
        await message.reply(f"echo '{message}'")


def start_bot():
    scheduler_message = SchedulerMessage(bot, subscribers)

    all_items = messages_builder.import_scheduler()
    for hour, minutes, message_file_name in all_items:
        cloned_message_file_name = message_file_name[:]
        message_func = lambda:messages_builder.get_message(cloned_message_file_name)
        scheduler_message.add_event(hour=hour, minutes=minutes, message_func=message_func)
    scheduler_message.add_event(hour=9, minutes=0, message_func=messages_builder.get_daily_message)
    # scheduler_message.add_polling(custom_polling_func=red_alert_checking, sleep_seconds=1)

    executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
