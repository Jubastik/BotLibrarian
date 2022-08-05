from tgbot.services.db import db_session
from tgbot.services.db.scripts import Response
from tgbot.services.db.sql_models import User, Genre, Book, BookGenres
from tgbot.services.scripts import MyBook


async def register_user(tg_id: int, tg_name: str, tg_username: str) -> Response:
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.tg_id == tg_id).first()
    if user is None:
        user = User(tg_id=tg_id, tg_name=tg_name, tg_username=tg_username)
        db_sess.add(user)
        db_sess.commit()
    db_sess.close()
    return Response(True, [])


async def get_my_books(tg_id: int) -> Response:
    db_sess = db_session.create_session()
    books = db_sess.query(Book).join('user').filter(User.tg_id == tg_id).all()
    list_of_books = []
    for book in books:
        # Сортировка по значимости жанра в данной книги
        genres = sorted([[g.genre.name, g.weight] for g in book.genres_m], key=lambda x: x[1])
        genres = [g[0] for g in genres]
        b = MyBook(book.user_id, book.id, book.title, book.author, genres, book.note)
        list_of_books.append(b)
    db_sess.close()
    return Response(True, list_of_books)


async def get_all_genres() -> Response:
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    list_of_genres = [(g.id, g.name) for g in genres]
    db_sess.close()
    return Response(True, list_of_genres)


async def get_genre_name(genre_id: int) -> Response:
    db_sess = db_session.create_session()
    genre_name = db_sess.query(Genre.name).filter(Genre.id == genre_id).first()
    if genre_name is not None:
        genre_name = genre_name[0]
    db_sess.close()
    return Response(True, [genre_name])


async def get_bookshelf(genres: list) -> Response:
    db_sess = db_session.create_session()
    if 'all' in [_[0] for _ in genres]:
        books = db_sess.query(Book).all()
    else:
        books = db_sess.query(Book).join(BookGenres).join(Genre).filter(Genre.id.in_([_[0] for _ in genres])).all()
    if len(books) == 0:
        return Response(False, ['Книги не найдено'])
    list_of_books = []
    for book in books:
        # Сортировка по значимости жанра в данной книги
        genres = sorted([[g.genre.name, g.weight] for g in book.genres_m], key=lambda x: x[1])
        genres = [g[0] for g in genres]
        b = MyBook(book.user_id, book.id, book.title, book.author, genres, book.note, book.user.tg_name,
                   book.user.tg_username)
        list_of_books.append(b)
    db_sess.close()
    return Response(True, list_of_books)


async def save_book(book: MyBook) -> Response:
    db_sess = db_session.create_session()
    user_id = db_sess.query(User.id).filter(User.tg_id == book.tg_id).first()[0]
    bd_book = Book(
        title=book.title,
        author=book.author,
        note=book.note,
        user_id=user_id,
    )
    db_sess.add(bd_book)
    db_sess.flush()
    for num, genre in enumerate(book.genres):
        genre_id = db_sess.query(Genre.id).filter(Genre.name == genre).first()
        if genre_id is None:
            g = Genre(name=genre)
            db_sess.add(g)
            db_sess.flush()
            genre_id = g.id
        else:
            genre_id = genre_id[0]
        db_sess.add(BookGenres(weight=num, book_id=bd_book.id,
                               genre_id=genre_id))
    db_sess.commit()
    db_sess.close()
    return Response(True, [str(book)])


async def del_book(tg_id: int, book_id: int) -> Response:
    db_sess = db_session.create_session()
    book = db_sess.query(Book).filter(Book.id == book_id).first()
    if book.user.tg_id != tg_id:
        db_sess.close()
        return Response(False, ['Вы не можете удалить эту книгу'])
    db_sess.delete(book)
    db_sess.commit()
    db_sess.close()
    return Response(True, [])
