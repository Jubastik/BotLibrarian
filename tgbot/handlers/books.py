from aiogram.types import Message, CallbackQuery

from bot import dp, bot
from tgbot.FSM.states import UserMenu, AddBook
from tgbot.handlers.menu import query_menu
from tgbot.keyboards.inline.markup import get_markup_my_books, get_markup_go_to_menu, get_markup_save_genres, \
    get_markup_user_menu, get_markup_save_book
from tgbot.services.db.methods import get_my_books, save_book
from tgbot.services.scripts import update_msg, MyBook


@dp.callback_query_handler(state=UserMenu.Menu, text='my_books')
async def handler_my_books(call: CallbackQuery):
    await UserMenu.MyBooks.set()
    res = await get_my_books(call.from_user.id)
    await res.check_correctness(call)

    text = [f'Ваши книги: \n id/Название/автор/жанр/записка']
    for book in res.data:
        text.append(f'{book.id}, {book.title}, {book.author}, {";".join(book.genres)}, {book.note}')
    text = '\n---------------------------\n'.join(text)
    await update_msg(text, get_markup_my_books(), call)

    await call.answer()


@dp.callback_query_handler(state=UserMenu.MyBooks, text='add_book')
async def handler_add_book_init(call: CallbackQuery):
    await AddBook.Title.set()
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["book"] = MyBook(call.from_user.id)
    text = 'Введите название книги'
    await update_msg(text, get_markup_go_to_menu(), call)
    await call.answer()


@dp.message_handler(state=AddBook.Title, content_types=['text'])
async def handler_add_title(msg: Message):
    await AddBook.Author.set()
    FSMContext = dp.current_state(user=msg.from_user.id)
    text = 'Введите автора книги'
    async with FSMContext.proxy() as FSMdata:
        await FSMdata["book"].add_title(msg.text)
        msg = await msg.answer(text, reply_markup=get_markup_go_to_menu())
        FSMdata["main_msg_id"] = msg.message_id


@dp.message_handler(state=AddBook.Author, content_types=['text'])
async def handler_add_author(msg: Message):
    await AddBook.Genre.set()
    FSMContext = dp.current_state(user=msg.from_user.id)
    text = 'Введите жанры книги'
    async with FSMContext.proxy() as FSMdata:
        await FSMdata["book"].add_author(msg.text)
        msg = await msg.answer(text, reply_markup=get_markup_save_genres())
        FSMdata["main_msg_id"] = msg.message_id


@dp.message_handler(state=AddBook.Genre, content_types=['text'])
async def handler_add_genre(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        await FSMdata["book"].add_genre(msg.text)


@dp.callback_query_handler(state=AddBook.Genre, text='save_genres')
async def handler_save_genres(call: CallbackQuery):
    await AddBook.Note.set()
    FSMContext = dp.current_state(user=call.from_user.id)
    text = 'Оставьте пожелания'
    msg = await bot.send_message(call.message.chat.id, text)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["main_msg_id"] = msg.message_id
    await update_msg(text, get_markup_go_to_menu(), call)
    await call.answer()


@dp.message_handler(state=AddBook.Note, content_types=['text'])
async def handler_add_note(msg: Message):
    await AddBook.Finish.set()
    FSMContext = dp.current_state(user=msg.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        await FSMdata["book"].add_note(msg.text)
        text = f'Все ли верно? \n {FSMdata["book"]}'
        msg = await msg.answer(text, reply_markup=get_markup_save_book())
        FSMdata["main_msg_id"] = msg.message_id


@dp.callback_query_handler(state=AddBook.Finish, text='save_book')
async def handler_save_genres(call: CallbackQuery):
    await UserMenu.Menu.set()
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        res = await save_book(FSMdata["book"])
        await res.check_correctness(call)
    await call.answer()
    await query_menu(call)
