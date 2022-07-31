from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMenu(StatesGroup):
    Menu = State()
    MyBooks = State()


class Bookshelf(StatesGroup):
    Init = State()
    Finish = State()


class AddBook(StatesGroup):
    Title = State()
    Author = State()
    Genre = State()
    Note = State()
    Finish = State()


class DelBook(StatesGroup):
    Init = State()
    Delete = State()
