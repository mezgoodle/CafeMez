from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.location import create_markup as location_markup
from tgbot.keyboards.inline.places_keyboard import create_markup as places_markup


@dp.message_handler(Command('rs'))
async def find_restaurants(message: Message) -> Message:
    markup = location_markup()
    return await message.answer('Send location by button or just as input', reply_markup=markup)


@dp.message_handler(Command('places'))
async def show_places(message: Message) -> Message:
    markup = places_markup()
    return await message.answer('Оберіть вільне місце, яке хочете забронювати', reply_markup=markup)
