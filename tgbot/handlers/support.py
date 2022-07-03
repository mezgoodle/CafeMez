from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.inline.support_keyboard import create_keyboard


@dp.message_handler(Command('support'))
async def ask_support(message: Message) -> Message:
    text = 'Виникла проблема? Натисніть кнопку нижче!'
    keyboard = await create_keyboard(messages='one')
    return await message.answer(text, reply_markup=keyboard)
