import logging
from aiogram.utils import executor
from dotenv import load_dotenv
import os

# preload
load_dotenv()

import tgbot
from tgbot import filters, handlers
from bot import dp


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    tgbot.filters.setup(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == "__main__":
    start()
