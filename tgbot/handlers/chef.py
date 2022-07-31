from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import User
from tgbot.keyboards.inline.orders import orders_keyboard


@dp.message_handler(Command("my_orders"), is_chef=True)
async def show_orders(message: Message):
    api: User = message.bot.get('users_api')
    orders = await api.get_orders(message.from_user.username)
    for order in orders:
        text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
        keyboard = orders_keyboard(order)
        await message.answer(text, reply_markup=keyboard)
    return await message.answer(f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n'
                                f'Щоб змінити статус замовлення - {hbold("натисніть на кнопку Готове або Не готове")}\n'
                                f'Щоб змінити статус оплати - {hbold("натисніть на кнопку Оплачено або Не оплачено")}\n'
                                f'Щоб видалити замовлення - {hbold("натисніть на кнопку Видалити")}')
