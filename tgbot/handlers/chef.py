from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import Order
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.keyboards.inline.callback_data import order_callback


@dp.message_handler(Command("my_orders"), is_chef=True)
async def show_orders(message: Message):
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


@dp.callback_query_handler(order_callback.filter(action='show'), is_chef=True)
@dp.callback_query_handler(order_callback.filter(action='show'), is_courier=True)
async def show_order_item(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    item = await api.get_order_item(callback_data['id'])
    # TODO: send here the photo of the item
    text = f'{hbold(item["item"]["name"])}\n' \
           f'{hbold("Кількість:")} {item["quantity"]}\n' \
           f'{hbold("Ціна за шт.:")} {item["item"]["price"]} грн.'
    # return await callback_query.message.answer_photo(photo=item['item']['photo'], caption=text)
    return await callback_query.message.answer(text)


@dp.callback_query_handler(order_callback.filter(action='paid'), is_chef=True)
@dp.callback_query_handler(order_callback.filter(action='paid'), is_courier=True)
async def change_order_payment(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    new_order, status = await api.update_order(
        callback_data['id'],
        {'is_paid': callback_data['value']}
    )
    if status == 200:
        keyboard = orders_keyboard(new_order)
        await callback_query.message.answer('Статус оплати змінено!')
        return await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    return await callback_query.message.answer('Помилка при зміні статусу оплати!')


@dp.callback_query_handler(order_callback.filter(action='ready'), is_chef=True)
async def change_order_ready(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    new_order, status = await api.update_order(
        callback_data['id'],
        {'is_ready': callback_data['value']}
    )
    if status == 200:
        keyboard = orders_keyboard(new_order)
        await callback_query.message.answer('Статус приготування змінено!')
        return await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    return await callback_query.message.answer('Помилка при зміні статусу приготування!')


@dp.callback_query_handler(order_callback.filter(action='delete'), is_chef=True)
async def delete_order(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    status = await api.delete_order(callback_data['id'])
    if status == 204:
        return await callback_query.message.answer('Замовлення успішно видалено!')
    return await callback_query.message.answer('Помилка при видалення замовлення!')
