from aiogram.types import CallbackQuery

from bot import dp
from tgbot.FSM.states import UserMenu
from tgbot.keyboards.inline.markup import get_markup_my_books, get_markup_bookshelf
from tgbot.services.db.methods import get_bookshelf
from tgbot.services.scripts import update_msg


@dp.callback_query_handler(state=UserMenu.Menu, text='bookshelf')
async def handler_bookshelf(call: CallbackQuery):
    await UserMenu.Bookshelf.set()
    res = await get_bookshelf()
    await res.check_correctness(call)

    text = [f'Книжная полка: \n id/Название/автор/жанр/записка']
    for book in res.data:
        text.append(f'{book[0]}, {book[1]}, {book[2]}, {book[3]}')
    text = '\n'.join(text)
    await update_msg(text, get_markup_bookshelf(), call)
    await call.answer()