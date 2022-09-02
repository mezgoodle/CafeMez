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


@dp.callback_query_handler(order_callback.filter(action='paid'), is_admin=True)
@dp.callback_query_handler(order_callback.filter(action='paid'), is_courier=True)
async def change_order_payment(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    order = await api.get_order(callback_data['id'])
    if order['connected_courier'] == callback_query.from_user.username:
        new_order, status = await api.update_order(
            callback_data['id'],
            {'is_paid': callback_data['value']}
        )
        if status == 200:
            keyboard = orders_keyboard(new_order)
            await callback_query.message.answer('Статус оплати змінено!')
            return await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        return await callback_query.message.answer('Помилка при зміні статусу оплати!')


@dp.callback_query_handler(order_callback.filter(action='delivered'), is_courier=True)
async def change_order_delivered(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    bot: Bot = callback_query.bot
    order = await api.get_order(callback_data['id'])
    if order['connected_courier'] == callback_query.from_user.username:
        new_order, status = await api.update_order(
            callback_data['id'],
            {'is_delivered': callback_data['value']}
        )
        if status == 200:
            keyboard = orders_keyboard(new_order)
            await bot.send_message(order['user']['telegram_id'], 'Ваше замовлення доставлене')
            await callback_query.message.answer('Статус доставки змінено!')
            return await callback_query.message.edit_reply_markup(reply_markup=keyboard)
        return await callback_query.message.answer('Помилка при зміні статусу доставки!')


@dp.callback_query_handler(order_callback.filter(action='coords'), is_courier=True)
@dp.callback_query_handler(order_callback.filter(action='coords'), is_registered=True)
async def show_order_coords(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    order = await api.get_order(callback_data['id'])
    long, lat = order['shipping_address_longitude'], order['shipping_address_latitude']
    return await callback_query.message.answer_location(lat, long)


@dp.message_handler(Command("my_order"), is_courier=True)
async def show_courier_order(message: Message):
    api: Order = message.bot.get('orders_api')
    order = await api.get_order_by_courier(message.from_user.username)
    if 'detail' not in order.keys():
        text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
        keyboard = orders_keyboard(order)
        await message.answer(text, reply_markup=keyboard)
        return await message.answer(f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n')
    return await message.answer('У вас немає замовлень')


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
