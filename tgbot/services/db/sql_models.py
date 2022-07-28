import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import Session

from . import db_session
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = "user"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    tg_name = sqlalchemy.Column(sqlalchemy.String)
    books = orm.relationship("Book", back_populates="user")

    def __repr__(self):
        return f"<User> {self.id} {self.tg_name} {self.tg_id}"


class Book(SqlAlchemyBase):
    __tablename__ = "book"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    author = sqlalchemy.Column(sqlalchemy.String)
    note = sqlalchemy.Column(sqlalchemy.String)
    genres_m = orm.relationship("BookGenres", cascade="all, delete-orphan")
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("user.id"))
    user = orm.relationship("User", back_populates="books")

    def __repr__(self):
        return f"<Book> {self.id} {self.title} {self.author} {self.note}"


class BookGenres(SqlAlchemyBase):
    __tablename__ = "book_genres"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    weight = sqlalchemy.Column(sqlalchemy.Integer)
    book_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("book.id"), nullable=False)
    genre_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("genre.id"), nullable=False)
    genre = orm.relationship("Genre", viewonly=True)


class Genre(SqlAlchemyBase):
    __tablename__ = "genre"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre> {self.id} {self.name}"
