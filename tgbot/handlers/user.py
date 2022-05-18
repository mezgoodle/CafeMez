import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.keyboards.reply.location import create_markup


@dp.message_handler(Command('rs'))
async def find_restaurants(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    markup = create_markup()
    return await message.answer('Send location by button or just as input', reply_markup=markup)
