from aiogram.types import Message

from loader import dp


@dp.message_handler()
async def echo(message: Message) -> Message:
    return await message.answer(message.text)
