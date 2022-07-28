from bot import dp
from tgbot.FSM.states import UserMenu


class Response:
    def __init__(self, success: bool, data: list):
        self.success = success
        self.data = data

    async def check_correctness(self, call):
        if not self.success:
            await call.answer('Что-то пошло не так... ' + " ".join(self.data))
            await UserMenu.Menu.set()

    async def get_data(self):
        return self.data
