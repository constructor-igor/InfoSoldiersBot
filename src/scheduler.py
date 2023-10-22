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

    def add_event(self, hour, minutes):
        self.loop.create_task(self.send_scheduled_message(hour, minutes))

    async def send_scheduled_message(self, hour, minutes):
        message = 'שלום לכולם! למי שמעוניין בדרך חוץ מכסף לתמוך בחיילים החטופים ובעם ישראל, מומלץ לקרוא פרקי תהילים במלחמה לשם ביטחון. \
    תהילים פרק קכ"א  \
    [https://tehilim.co/chapter/121/] \
    תהילים פרק ק"ל \
    [https://tehilim.co/chapter/130/] \
    המשך יום טוב .👋'
        while True:
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minutes, second=0, microsecond=0)
            time_until_target = target_time - now
            if time_until_target.total_seconds() < 0:
                target_time += timedelta(days=1)
            await asyncio.sleep((target_time - datetime.now()).total_seconds())
            for chat_id in self.subscribers.get_all():
                await self.bot.send_message(chat_id=chat_id, text=message)
            logging.info("Scheduled message sent.")
