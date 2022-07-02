from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from aiogram.types import ChatType

from loader import dp

from re import compile


@dp.message_handler(CommandStart(deep_link=compile(r'^[a-z0-9_-]{3,15}$')), ChatTypeFilter(ChatType.PRIVATE))
async def register_referral(message: Message):
    referral = message.get_args()
    await message.answer(referral)


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    return await message.answer("Hello, I'm a bot!")
