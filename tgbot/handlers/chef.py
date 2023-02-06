from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.keyboards.inline.callback_data import order_callback
from tgbot.misc.staff_actions import show_item, show_orders_message, staff_action


@dp.message_handler(Command("orders"), is_courier=True)
@dp.message_handler(Command("orders"), is_chef=True)
async def show_orders(message: Message):
    return await show_orders_message(message)


@dp.callback_query_handler(order_callback.filter(action="show"), is_registered=True)
async def show_order_item(callback_query: CallbackQuery, callback_data: dict):
    return await show_item(callback_query, callback_data)


@dp.callback_query_handler(order_callback.filter(action="ready"), is_chef=True)
async def change_order_ready(callback_query: CallbackQuery, callback_data: dict):
    additional_text = (
        f'Статус вашого замовлення із номером {callback_data["id"]} '
        f'змінено на {hbold("готове") if callback_data["value"] == "True" else hbold("не готове")}"!'
    )
    return await staff_action(
        callback_query,
        callback_data,
        {"is_ready": callback_data["value"]},
        "Статус приготування змінено!",
        "Помилка при зміні статусу приготування!",
        additional_text=additional_text,
    )
