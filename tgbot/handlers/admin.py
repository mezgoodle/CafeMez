from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command(['stats']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    return await message.reply(f'Hello, {message.from_user.username}!')


@dp.message_handler(content_types=ContentType.LOCATION, is_general_admin=True)
async def add_cafe_coords(message: Message) -> Message:
    # TODO: send request to server
    return await message.reply(f'{message.location.longitude}, {message.location.latitude}')
