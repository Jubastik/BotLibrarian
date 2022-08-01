from bot import dp
from tgbot.services.db.scripts import ResponseError


@dp.errors_handler(exception=ResponseError)
async def errors_handler(update, error):
    return True
