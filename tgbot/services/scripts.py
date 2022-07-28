from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot import dp, bot


class MyBook:
    def __init__(self, tg_id: int, id: int = None, title: str = None, author: str = None, genres: list = [],
                 note: str = None):
        self.tg_id = tg_id
        self.id = id
        self.title = title
        self.author = author
        self.genres = genres
        self.note = note

    async def add_title(self, title: str):
        self.title = title
        return True

    async def add_author(self, author: str):
        self.author = author
        return True

    async def add_genre(self, genre: str):
        self.genres.append(genre.lower())
        return True

    async def add_note(self, note: str):
        self.note = note
        return True

    def __str__(self):
        return f'{self.tg_id}, {self.title}, {self.author}, {self.genres}, {self.note}'


async def update_msg(text: str, reply_markup: InlineKeyboardMarkup, call: CallbackQuery):
    # Обновление главного сообщения
    FSMContext = dp.current_state(user=call.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = call.from_user.id
        await bot.edit_message_text(
            text,
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=reply_markup,
        )
