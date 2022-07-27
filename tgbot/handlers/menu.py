from aiogram.types import Message, CallbackQuery

from bot import dp
from tgbot.FSM.states import UserMenu
from tgbot.keyboards.inline.markup import get_markup_user_menu
from tgbot.services.scripts import update_msg


@dp.message_handler(commands=['start', 'menu'], state='*')
async def handler_menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.finish()
    await UserMenu.Menu.set()
    async with FSMContext.proxy() as FSMdata:
        msg = await msg.answer(
            "Привет", reply_markup=get_markup_user_menu())
        FSMdata["main_msg_id"] = msg.message_id


@dp.callback_query_handler(state="*", text="menu")
async def query_menu(call: CallbackQuery):
    await UserMenu.Menu.set()
    await update_msg("Привет", get_markup_user_menu(), call)
    await call.answer()
