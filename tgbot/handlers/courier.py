from aiogram import Bot
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import Order
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.keyboards.inline.callback_data import order_callback


@dp.message_handler(Command("orders"), is_courier=True)
async def show_courier_order(message: Message):
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


@dp.message_handler(Command("my_order"), is_courier=True)
async def show_courier_order(message: Message):
    pass


@dp.callback_query_handler(order_callback.filter(action='courier'), is_courier=True)
async def take_order(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    new_order, status = await api.update_order(callback_data['id'],
                                               {'connected_courier': callback_query.from_user.username})
    if status == 200:
        keyboard = orders_keyboard(new_order)
        bot: Bot = callback_query.bot
        await bot.send_message(new_order['user']['telegram_id'],
                               f'Ваше замовлення #{new_order["id"]} узяв кур\'єр @{callback_query.from_user.username}')
        await callback_query.message.answer('Ви успішно взяли замовлення!')
        return await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    return await callback_query.message.answer('Помилка при взятті замовлення!')
