from aiogram.types import CallbackQuery

from tgbot.FSM.states import UserMenu
from tgbot.keyboards.inline.markup import get_markup_user_menu
from tgbot.services.scripts import update_msg


async def err_query_menu(call: CallbackQuery):
    await UserMenu.Menu.set()
    await update_msg("Привет! Используй <b> Мои книги </b> если хочешь поделиться книгой, "
                     "а если хочешь получить книгу, используй <b> Книжная полка </b>.",
                     get_markup_user_menu(), call)
    await call.answer()
