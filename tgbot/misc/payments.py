from random import choice
from typing import Union

from aiogram import Bot
from aiogram.types import Message, PreCheckoutQuery
from aiogram.utils.markdown import hbold

from tgbot.misc.backend import Order, Place, User


async def handle_place_payment(
    query: PreCheckoutQuery, data: list, username: str
) -> Message:
    bot: Bot = query.bot
    places_api: Place = bot.get("places_api")
    return await handle_payment(
        query,
        places_api,
        data[2],
        {"free": False, "customer": username},
        data[1],
        "staff",
    )


async def handle_order_payment(query: PreCheckoutQuery, data: list, *args):
    bot: Bot = query.bot
    order_api: Order = bot.get("orders_api")
    return await handle_payment(
        query, order_api, data[2], {"is_paid": True}, data[1], "chefs"
    )


async def handle_payment(
    query: PreCheckoutQuery,
    api: Union[Order, Place],
    restaurant_name: str,
    data: dict,
    object_id: str,
    type_of_staff: str,
):
    bot: Bot = query.bot
    users_api: User = bot.get("users_api")
    if type(api).__name__ == Order.__name__:
        _, status = await api.update_order(object_id, data)
        text = f"Нове замовлення з номером {hbold(object_id)}"
    else:
        _, status = await api.update_place(object_id, data)
        text = f"Столик із номером {hbold(object_id)} зарезервований"
    if status == 200:
        await bot.answer_pre_checkout_query(query.id, ok=True)
        admins = await users_api.get_staff(restaurant_name)
        admins = admins[type_of_staff]
        admin = choice(admins)
        await bot.send_message(admin["telegram_id"], text)
        return await bot.send_message(
            query.from_user.id, "Замовлення успішне! Працюємо із грошима💰"
        )
    else:
        await bot.answer_pre_checkout_query(query.id, ok=False)
        return await bot.send_message(
            query.from_user.id,
            "Виникли помилка. Зверніться у службу підтримки",
        )
