from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenu(StatesGroup):
    Menu = State()
    MyBooks = State()
    Bookshelf = State()


class AddBook(StatesGroup):
    Title = State()
    Author = State()
    Genre = State()
    Note = State()
    Finish = State()


class DelBook(StatesGroup):
    Init = State()
    Delete = State()
