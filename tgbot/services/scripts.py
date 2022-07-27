from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from bot import dp, bot


async def update_msg(text: str, reply_markup: InlineKeyboardMarkup, call: CallbackQuery):
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
