from aiogram import Bot
from aiogram.types import PreCheckoutQuery, Message

from tgbot.misc.backend import Place, Order


async def handle_place_payment(query: PreCheckoutQuery, data: list, username: str) -> Message:
    bot: Bot = query.bot
    api: Place = bot.get('places_api')
    _, status = await api.update_place(data[1], {'free': False, 'customer': username})
    if status == 200:
        await bot.answer_pre_checkout_query(query.id, ok=True)
        return await bot.send_message(query.from_user.id, "Оренда успішна! Працюємо із грошима💰")
    else:
        await bot.answer_pre_checkout_query(query.id, ok=False)
        return await bot.send_message(query.from_user.id, "Виникли помилка. Зверніться у службу підтримки")


async def handle_order_payment(query: PreCheckoutQuery, data: list, username: str):
    pass
