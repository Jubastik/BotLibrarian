from aiogram.types import CallbackQuery

from bot import dp
from tgbot.FSM.states import UserMenu
from tgbot.keyboards.inline.markup import get_markup_my_books
from tgbot.services.db.methods import get_my_books
from tgbot.services.scripts import update_msg


@dp.callback_query_handler(state=UserMenu.Menu, text='my_books')
async def handler_my_books(call: CallbackQuery):
    await UserMenu.MyBooks.set()
    res = await get_my_books(call.from_user.id)
    await res.check_correctness(call)

    text = [f'Ваши книги: \n Название/автор/жанр/записка']
    for book in res.data:
        text.append(f'{book[0]}, {book[1]}, {book[2]}, {book[3]}')
    text = '\n'.join(text)
    await update_msg(text, get_markup_my_books(), call)

    await call.answer()
