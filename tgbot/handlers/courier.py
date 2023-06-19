from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.keyboards.inline.callback_data import order_callback
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.misc.backend import Order
from tgbot.misc.staff_actions import finish_order_action, staff_action


@dp.callback_query_handler(
    order_callback.filter(action="paid"), is_courier=True
)
async def change_order_payment(
    callback_query: CallbackQuery, callback_data: dict
):
    return await staff_action(
        callback_query,
        callback_data,
        {"is_paid": callback_data["value"]},
        "Статус оплати змінено!",
        "Помилка при зміні статусу оплати!",
        True,
    )


@dp.callback_query_handler(
    order_callback.filter(action="delivered"), is_courier=True
)
async def change_order_delivered(
    callback_query: CallbackQuery, callback_data: dict
):
    additional_text = (
        f'Статус доставки вашого замовлення із номером {callback_data["id"]} '
        f'змінено на {hbold("доставлене") if callback_data["value"] == "True" else hbold("не доставлене")}"!'
    )
    return await staff_action(
        callback_query,
        callback_data,
        {"is_delivered": callback_data["value"]},
        "Статус доставки змінено!",
        "Помилка при зміні статусу доставки!",
        True,
        additional_text,
    )


@dp.callback_query_handler(
    order_callback.filter(action="coords"), is_courier=True
)
@dp.callback_query_handler(
    order_callback.filter(action="coords"), is_registered=True
)
async def show_order_coords(
    callback_query: CallbackQuery, callback_data: dict
):
    api: Order = callback_query.bot.get("orders_api")
    order = await api.get_order(callback_data["id"])
    long, lat = (
        order["shipping_address_longitude"],
        order["shipping_address_latitude"],
    )
    return await callback_query.message.answer_location(lat, long)


@dp.message_handler(Command("my_order"), is_courier=True)
async def show_courier_order(message: Message):
    api: Order = message.bot.get("orders_api")
    order = await api.get_order_by_courier(message.from_user.username)
    if "detail" not in order.keys():
        text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
        keyboard = orders_keyboard(order)
        await message.answer(text, reply_markup=keyboard)
        return await message.answer(
            f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n'
        )
    return await message.answer("У вас немає замовлень")


@dp.callback_query_handler(
    order_callback.filter(action="courier"), is_courier=True
)
async def take_order(callback_query: CallbackQuery, callback_data: dict):
    additional_text = f'Ваше замовлення #{callback_data["id"]} узяв кур\'єр @{callback_query.from_user.username}'
    return await staff_action(
        callback_query,
        callback_data,
        {"connected_courier": callback_query.from_user.username},
        "Ви успішно взяли замовлення!",
        "Помилка при взятті замовлення!",
        additional_text=additional_text,
    )


@dp.callback_query_handler(
    order_callback.filter(action="finished"), is_courier=True
)
async def finish_order(callback_query: CallbackQuery, callback_data: dict):
    return await finish_order_action(
        callback_query,
        callback_data,
        "Статус замовлення змінено!",
        "Помилка при зміні статусу замовлення!",
        True,
    )
