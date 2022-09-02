from aiogram.types import Message
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.misc.backend import Order


async def show_orders_message(message: Message) -> Message:
    api: Order = message.bot.get('orders_api')
    orders = await api.get_orders(message.from_user.username)
    if orders:
        for order in orders:
            text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
            keyboard = orders_keyboard(order)
            await message.answer(text, reply_markup=keyboard)
        return await message.answer(f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n'
                                    f'Щоб змінити статус замовлення - {hbold("натисніть на кнопку Готове або Не готове")}\n'
                                    f'Щоб змінити статус оплати - {hbold("натисніть на кнопку Оплачено або Не оплачено")}\n'
                                    f'Щоб видалити замовлення - {hbold("натисніть на кнопку Видалити")}')
    return await message.answer('На даний момент немає замовлень')
