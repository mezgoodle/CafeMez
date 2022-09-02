from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import Order
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.keyboards.inline.callback_data import order_callback
from tgbot.misc.orders import show_orders_message


@dp.message_handler(Command("orders"), is_chef=True)
async def show_orders(message: Message):
    return await show_orders_message(message)


@dp.callback_query_handler(order_callback.filter(action='show'), is_chef=True)
@dp.callback_query_handler(order_callback.filter(action='show'), is_courier=True)
@dp.callback_query_handler(order_callback.filter(action='show'), is_admin=True)
async def show_order_item(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    item = await api.get_order_item(callback_data['id'])
    # TODO: send here the photo of the item
    text = f'{hbold(item["item"]["name"])}\n' \
           f'{hbold("Кількість:")} {item["quantity"]}\n' \
           f'{hbold("Ціна за шт.:")} {item["item"]["price"]} грн.'
    # return await callback_query.message.answer_photo(photo=item['item']['photo'], caption=text)
    return await callback_query.message.answer(text)


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


@dp.callback_query_handler(order_callback.filter(action='delete'), is_admin=True)
async def delete_order(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    status = await api.delete_order(callback_data['id'])
    if status == 204:
        await callback_query.message.delete()
        return await callback_query.message.answer('Замовлення успішно видалено!')
    return await callback_query.message.answer('Помилка при видалення замовлення!')
