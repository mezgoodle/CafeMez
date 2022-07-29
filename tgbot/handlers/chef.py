from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.misc.backend import User


@dp.message_handler(Command("my_orders"), is_chef=True)
async def show_orders(message: Message):
    api: User = message.bot.get('users_api')
    orders = await api.get_orders(message.from_user.username)
    return await message.answer(f'Ваші замовлення:\n{orders}')