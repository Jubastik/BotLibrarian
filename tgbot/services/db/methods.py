from tgbot.services.db.scripts import Response

temp_book = [1233, 'Война и мир', 'Толстой', ['Роман', 'Детектив'], 'Описание книги']


async def get_my_books(tg_id: int) -> Response:
    return Response(True, [temp_book])


async def get_bookshelf() -> Response:
    return Response(True, [temp_book])
