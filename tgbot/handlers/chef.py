from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import Order
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.keyboards.inline.callback_data import order_callback


@dp.message_handler(Command("my_orders"), is_chef=True)
async def show_orders(message: Message):
    api: Order = message.bot.get('orders_api')
    orders = await api.get_orders(message.from_user.username)
    for order in orders:
        text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
        keyboard = orders_keyboard(order)
        await message.answer(text, reply_markup=keyboard)
    return await message.answer(f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n'
                                f'Щоб змінити статус замовлення - {hbold("натисніть на кнопку Готове або Не готове")}\n'
                                f'Щоб змінити статус оплати - {hbold("натисніть на кнопку Оплачено або Не оплачено")}\n'
                                f'Щоб видалити замовлення - {hbold("натисніть на кнопку Видалити")}')


@dp.callback_query_handler(order_callback.filter(action='show'), is_chef=True)
async def show_order_item(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    # TODO: send here the photo of the item
    item = await api.get_order_item(callback_data['id'])
    return await callback_query.message.answer(f'{hbold(item["item"]["name"])}\n'
                                               f'{hbold("Кількість:" )} {item["quantity"]}\n'
                                               f'{hbold("Ціна за шт.:")} {item["item"]["price"]} грн.')


@dp.callback_query_handler(order_callback.filter(action='paid'), is_chef=True)
async def change_order_payment(callback_query: CallbackQuery, callback_data: dict):
    # api: Order = callback_query.bot.get('orders_api')
    print(callback_data)


@dp.callback_query_handler(order_callback.filter(action='ready'), is_chef=True)
async def change_order_ready(callback_query: CallbackQuery, callback_data: dict):
    # api: Order = callback_query.bot.get('orders_api')
    print(callback_data)
