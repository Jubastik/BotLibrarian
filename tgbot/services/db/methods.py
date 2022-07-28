from tgbot.services.db.scripts import Response
from tgbot.services.scripts import Book

temp_book = [1233, 'Война и мир', 'Толстой', ['Роман', 'Детектив'], 'Описание книги']


async def get_my_books(tg_id: int) -> Response:
    return Response(True, [temp_book])


async def get_bookshelf() -> Response:
    return Response(True, [temp_book])


async def save_book(tg_id: int, book: Book) -> Response:
    print(f"Книга сохранена {str(book)}")
    return Response(True, [str(book)])
