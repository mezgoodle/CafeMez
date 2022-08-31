from aiogram import Bot
from aiogram.types import PreCheckoutQuery, Message
from aiogram.utils.markdown import hbold

from tgbot.misc.backend import Place, Order, User

from random import choice


async def handle_place_payment(query: PreCheckoutQuery, data: list, username: str) -> Message:
    bot: Bot = query.bot
    users_api: User = bot.get('users_api')
    places_api: Place = bot.get('places_api')
    place_id = data[1]
    rs_name = data[2]
    _, status = await places_api.update_place(place_id, {'free': False, 'customer': username})
    if status == 200:
        await bot.answer_pre_checkout_query(query.id, ok=True)
        staff = await users_api.get_staff(rs_name)
        staff = staff['staff']
        admin = choice(staff)
        await bot.send_message(admin['telegram_id'],
                               f'Столик із номером {hbold(place_id)} у ресторані {hbold(rs_name)} зарезервований')
        return await bot.send_message(query.from_user.id, "Оренда успішна! Працюємо із грошима💰")
    else:
        await bot.answer_pre_checkout_query(query.id, ok=False)
        return await bot.send_message(query.from_user.id, "Виникли помилка. Зверніться у службу підтримки")


async def handle_order_payment(query: PreCheckoutQuery, data: list, username: str):
    pass
