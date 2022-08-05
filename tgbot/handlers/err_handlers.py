import os

from aiogram.utils.exceptions import TelegramAPIError

from bot import dp, bot
from tgbot.services.db.scripts import ResponseError


@dp.errors_handler(exception=ResponseError)
async def errors_handler_response(update, error):
    return True


@dp.errors_handler(exception=Exception)
async def errors_handler_all(update, error):
    if os.getenv('SERVER_MODE', 'False') == 'True':
        chat_id = os.getenv("FEEDBACK_GROUP_ID")
        await bot.send_message(chat_id, f'Ошибка: {update}\nТекст: {error}')
