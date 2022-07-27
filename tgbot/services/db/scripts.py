from bot import dp
from tgbot.FSM.states import UserMenu


class Response:
    def __init__(self, success: bool, data: list):
        self.success = success
        self.data = data

    async def check_correctness(self, call):
        if not self.success:
            FSMContext = dp.current_state(user=call.from_user.id)
            await FSMContext.finish()
            await call.answer('Что-то пошло не так...')
            await UserMenu.Menu.set()
