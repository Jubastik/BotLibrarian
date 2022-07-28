from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def get_markup_user_menu() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Мои книги', callback_data='my_books'),
               InlineKeyboardButton(text='Книжная полка', callback_data='bookshelf'), ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_markup_my_books() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Добавить книгу', callback_data='add_book'),
               InlineKeyboardButton(text='Удалить книгу', callback_data='del_book'),
               InlineKeyboardButton(text='Меню', callback_data='menu'), ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_markup_bookshelf() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Меню', callback_data='menu')]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_markup_del_book(books: list) -> InlineKeyboardMarkup:
    DelBookData = CallbackData('del_book', 'book_id')
    buttons = []
    for book in books:
        buttons.append(InlineKeyboardButton(text=book.title, callback_data=DelBookData.new(book_id=book.id)))
    keyboard = InlineKeyboardMarkup(row_width=4)
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='menu'))
    return keyboard


def get_markup_go_to_menu() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Отмена', callback_data='menu')]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_markup_save_genres() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Сохранить', callback_data='save_genres'),
               InlineKeyboardButton(text='Отмена', callback_data='menu')]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_markup_save_book() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Сохранить', callback_data='save_book'),
               InlineKeyboardButton(text='Отмена', callback_data='menu')]
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard
