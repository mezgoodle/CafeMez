from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp

import logging


@dp.message_handler(Command(['stats']), is_admin=True)
async def show_stats(message: Message) -> Message:
    logger = logging.getLogger(__name__)
    logger.info('Handler executed')
    return await message.reply(f'Hello, {message.from_user.username}!')
