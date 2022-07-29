from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from tgbot.misc.backend import User


@dp.message_handler(Command("orders"), is_courier=True)
async def show_courier_order(message: Message):
    api: User = message.bot.get('users_api')
    orders = await api.get_orders(message.from_user.username)
    return await message.answer(f'Ваші замовлення:\n{orders}')


@dp.message_handler(Command("my_order"), is_courier=True)
async def show_courier_order(message: Message):
    pass
