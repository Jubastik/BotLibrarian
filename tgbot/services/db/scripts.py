from aiogram.dispatcher import FSMContext

from bot import dp, bot
from tgbot.handlers.err_menu import err_query_menu


class ResponseError(Exception):
    pass


class Response:
    def __init__(self, success: bool, data: list):
        self.success = success
        self.data = data

    async def check_correctness(self, call):
        if not self.success:
            await call.answer('Что-то пошло не так... ' + " ".join(self.data), show_alert=True)
            await err_query_menu(call)
            raise ResponseError()

    async def get_data(self):
        return self.data
