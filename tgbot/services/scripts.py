from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot import dp, bot


class Book:
    def __init__(self):
        self.id = None
        self.title = None
        self.author = None
        self.genres = []
        self.note = None

    async def add_title(self, title: str):
        self.title = title
        return True

    async def add_author(self, author: str):
        self.author = author
        return True

    async def add_genre(self, genre: str):
        self.genres.append(genre)
        return True

    async def add_note(self, note: str):
        self.note = note
        return True

    def __str__(self):
        return f'{self.id}, {self.title}, {self.author}, {self.genres}, {self.note}'


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
