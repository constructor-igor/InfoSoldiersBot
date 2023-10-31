import logging
from datetime import datetime, timedelta
import asyncio
from aiogram import Bot

from .subscribers import Subscribers


class SchedulerMessage():
    def __init__(self, bot: Bot, subscribers: Subscribers) -> None:
        self.bot = bot
        self.subscribers = subscribers
        self.loop = asyncio.get_event_loop()

    def add_event(self, hour, minutes, message_func):
        self.loop.create_task(self.send_scheduled_message(hour, minutes, message_func))

    def add_polling(self, custom_polling_func, sleep_seconds=1):
        # self._run_polling(custom_polling_func, sleep_seconds)
        self.loop.create_task(self._run_polling(custom_polling_func, sleep_seconds))

    async def send_scheduled_message(self, hour, minutes, message_func):
        while True:
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minutes, second=0, microsecond=0)
            time_until_target = target_time - now
            if time_until_target.total_seconds() < 0:
                target_time += timedelta(days=1)
            await asyncio.sleep((target_time - datetime.now()).total_seconds())
            for chat_id in self.subscribers.get_all():
                await self.bot.send_message(chat_id=chat_id, text=message_func())
            logging.info("Scheduled message sent.")

    async def _run_polling(self, custom_polling_func, sleep_seconds):
        while True:
            if custom_polling_func():
                logging.info(f"red_alert detected ==> sending message to all subscribers")
                for chat_id in self.subscribers.get_all():
                    await self.bot.send_message(chat_id=chat_id, text="red alert", disable_notification=True)
            await asyncio.sleep(sleep_seconds)
