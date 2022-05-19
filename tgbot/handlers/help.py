from aiogram.types import Message
from aiogram.dispatcher.filters import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def help_command(message: Message) -> Message:
    return await message.reply(f'Hello, {message.from_user.username}!')
