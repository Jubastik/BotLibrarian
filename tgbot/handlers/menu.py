import asyncio
import os
from pprint import pprint

from aiogram.types import Message, CallbackQuery

from bot import dp, bot
from tgbot.FSM.states import UserMenu
from tgbot.keyboards.inline.markup import get_markup_user_menu
from tgbot.services.db.methods import register_user
from tgbot.services.scripts import update_msg


@dp.message_handler(commands=['menu'], state='*')
async def handler_menu(msg: Message):
    await register_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.username)
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.finish()
    await UserMenu.Menu.set()
    async with FSMContext.proxy() as FSMdata:
        msg = await msg.answer(
            "Привет! Используй <b> Мои книги </b> если хочешь поделиться книгой, "
            "а если хочешь получить книгу, используй <b> Книжная полка </b>.",
            reply_markup=get_markup_user_menu())
        FSMdata["main_msg_id"] = msg.message_id


@dp.message_handler(commands=['start'], state='*')
async def handler_start_msg(msg: Message):
    await bot.send_message(msg.from_user.id, text='Привет! Я бот для букшеринга на ЛШ 2022')
    await asyncio.sleep(2)
    text = 'Ты можешь как дарить, так и получать книги. Если возник любой вопрос, пиши - /feedback Суть вопроса'
    await bot.send_message(msg.from_user.id, text=text)
    await handler_menu(msg)


@dp.callback_query_handler(state="*", text="menu")
async def query_menu(call: CallbackQuery):
    await UserMenu.Menu.set()
    await update_msg("Привет! Используй <b> Мои книги </b> если хочешь поделиться книгой, "
                     "а если хочешь получить книгу, используй <b> Книжная полка </b>.",
                     get_markup_user_menu(), call)
    await call.answer()


@dp.message_handler(state="*", commands=["feedback"])
async def handler_user_feedback(msg: Message):
    feedback = msg.text[10::]
    chat_id = os.getenv("FEEDBACK_GROUP_ID")
    if len(feedback) != 0:
        text = f'От: {msg.from_user.username}\n{feedback}'
        await bot.send_message(chat_id, text)
        await msg.answer('Обратная связь отправлена')
    else:
        await msg.answer('Пустая обратная связь. Пример обратной связи: /feedback Как добавить книгу?')
