from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenu(StatesGroup):
    Menu = State()
    MyBooks = State()
    Bookshelf = State()