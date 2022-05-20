from aiogram.types import Message
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command(['stats']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    return await message.reply(f'Hello, {message.from_user.username}!')
