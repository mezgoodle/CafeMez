import logging

from aiogram.types import Message, ContentTypes

from loader import dp


@dp.message_handler(content_types=ContentTypes.LOCATION)
async def nearest_restaurants(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    print(message.location)
    return await message.answer('Hello')
