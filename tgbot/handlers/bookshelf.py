from aiogram.types import CallbackQuery

from bot import dp, bot
from tgbot.FSM.states import UserMenu, Bookshelf
from tgbot.handlers.menu import query_menu
from tgbot.keyboards.inline.markup import get_markup_my_books, get_markup_bookshelf, get_markup_add_genre_bookshelf
from tgbot.services.db.methods import get_bookshelf, get_all_genres, get_genre_name
from tgbot.services.scripts import update_msg


@dp.callback_query_handler(state=UserMenu.Menu, text='bookshelf')
async def handler_init_bookshelf(call: CallbackQuery):
    res = await get_all_genres()
    await res.check_correctness(call)
    all_genres = await res.get_data()
    await Bookshelf.Init.set()
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata['current_genres'] = []
        FSMdata['all_genres'] = all_genres

    text = f'Выберите подходящие вам жанры. Так же вы можете выбрать все жанры \n Выбранные жанры: отсутствуют'
    await update_msg(text, get_markup_add_genre_bookshelf(all_genres), call)
    await call.answer()


@dp.callback_query_handler(state=Bookshelf.Init, text_contains='add_genre_to_bookshelf')
async def handler_add_genre_to_bookshelf(call: CallbackQuery):
    genre_id = call.data.split(':')[1]
    if genre_id == 'all':
        genre_name = 'all'
    else:
        res = await get_genre_name(int(genre_id))
        await res.check_correctness(call)
        genre_name = await res.get_data()
        genre_name = genre_name[0]
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if (genre_id, genre_name) not in FSMdata['current_genres']:
            FSMdata['current_genres'].append((genre_id, genre_name))
        else:
            FSMdata['current_genres'].remove((genre_id, genre_name))
        text = f'Выберите подходящие вам жанры. Так же вы можете выбрать все жанры \n ' \
               f'Выбранные жанры: {"; ".join([_[1] for _ in FSMdata["current_genres"]])}'
        await update_msg(text, get_markup_add_genre_bookshelf(FSMdata['all_genres']), call)


@dp.callback_query_handler(state=Bookshelf.Init, text='show_bookshelf')
async def handler_show_bookshelf(call: CallbackQuery):
    await UserMenu.Menu.set()
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        res = await get_bookshelf(FSMdata['current_genres'])
        await res.check_correctness(call)
        books = await res.get_data()
    for num, book in enumerate(books):
        text = []
        if num == 0:
            text.append(f'Подходящие книги:')
        text.append(
            f'ID: {book.id} \nНазвание: {book.title} \nАвтор: {book.author} \n'
            f'Жанры: {";".join(book.genres)} \nЗаписка от дарителя: {book.note}')
        await bot.send_message(call.from_user.id, text="\n".join(text))
    msg = await bot.send_message(call.from_user.id, text='Ты милашка)')
    async with FSMContext.proxy() as FSMdata:
        FSMdata['main_msg_id'] = msg.message_id
    await call.answer()
    await query_menu(call)
