from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from aiogram.types import ChatType

from loader import dp

from re import compile


@dp.message_handler(CommandStart(deep_link=compile(r'^[0-9]{3,15}$')), ChatTypeFilter(ChatType.PRIVATE))
async def register_refferal(message: Message):
    refferal = message.get_args()
    await message.answer(refferal)


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    return await message.answer("Hello, I'm a bot!")
