from pprint import pprint

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.location import location_markup
from tgbot.keyboards.inline.places_keyboard import places_markup


@dp.message_handler(Command('rs'))
async def find_restaurants(message: Message) -> Message:
    markup = location_markup()
    return await message.answer('Надішліть локацію через кнопку або просто як вкладення', reply_markup=markup)


@dp.message_handler(Command('places'))
async def show_places(message: Message) -> Message:
    markup = await places_markup(message)
    await message.answer('Оберіть вільне місце, яке хочете забронювати', reply_markup=markup)
    return await message.reply('Оренда буде дійсна дві години від початку оренди')
