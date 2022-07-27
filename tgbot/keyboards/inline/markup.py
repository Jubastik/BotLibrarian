from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_markup_user_menu() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Мои книги', callback_data='my_books'),
               InlineKeyboardButton(text='Книжная полка', callback_data='bookshelf'), ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_markup_my_books() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text='Добавить книгу', callback_data='add_book'),
               InlineKeyboardButton(text='Удалить книгу', callback_data='delete_book'),
               InlineKeyboardButton(text='Меню', callback_data='menu'), ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
