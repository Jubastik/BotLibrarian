from aiogram.dispatcher import FSMContext

from bot import dp, bot
# from tgbot.handlers.menu import query_menu


class Response:
    def __init__(self, success: bool, data: list):
        self.success = success
        self.data = data

    async def check_correctness(self, call):
        if not self.success:
            await call.answer('Что-то пошло не так... ' + " ".join(self.data))
            msg = await bot.send_message(call.from_user.id, text='Ты милашка)')
            # async with FSMContext.proxy() as FSMdata:
            #     FSMdata['main_msg_id'] = msg.message_id
            # await query_menu(call)

    async def get_data(self):
        return self.data
