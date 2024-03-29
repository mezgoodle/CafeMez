from datetime import datetime

from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.utils.markdown import hbold, hitalic

from loader import bot, dp
from tgbot.keyboards.inline.callback_data import place_callback as place_data
from tgbot.keyboards.inline.places_keyboard import place_markup, places_markup
from tgbot.keyboards.inline.restaurants_keyboard import restaurants_markup
from tgbot.misc.backend import Referral, Restaurant, User
from tgbot.misc.invoices.invoice import Item


@dp.callback_query_handler(text="busy_place")
async def busy_place_callback(call: CallbackQuery) -> Message:
    return await call.message.answer("Це місце зайнято. Оберіть інше.")


@dp.callback_query_handler(text_contains="rs:")
async def place_callback(call: CallbackQuery) -> Message:
    restaurant_id = call.data.split(":")[1]
    api: Restaurant = call.bot.get("restaurants_api")
    status = await api.delete_restaurant(restaurant_id)
    if status == 204:
        restaurants = await api.get_all_restaurants()
        keyboard = await restaurants_markup(restaurants)
        text = (
            f'Список ресторанів у базі даних. Щоб видалити, {hbold("натисніть хрестик")} навпроти імені номеру'
            f" ресторану:\n"
        )
        for index, restaurant in enumerate(restaurants, start=1):
            text += f'{hitalic(index)}. {restaurant["name"]}\n'
        await call.message.edit_text(text, reply_markup=keyboard)
        return await call.message.answer(
            "Ресторан було видалено з бази даних."
        )
    return await call.message.answer("Помилка при видаленні ресторану.")


@dp.callback_query_handler(place_data.filter(choice="yes"))
async def accept_offer(call: CallbackQuery, callback_data: dict) -> Message:
    number = callback_data["number"]
    restaurant = callback_data["restaurant"]
    api: User = call.bot.get("users_api")
    user = await api.get_user(call.from_user.username)
    need_email = False
    prices = [LabeledPrice(label="Оренда столика", amount=100 * 100)]
    if "detail" in user.keys():
        need_email = True
    else:
        ref_api: Referral = call.bot.get("referrals_api")
        if discount := await ref_api.get_discount(call.from_user.username):
            prices.append(
                LabeledPrice(label="Знижка", amount=int(-100 * discount))
            )
    place_invoice = Item(
        title=f"Місце з номером {number}",
        description=f"Оренда місця з номером {number} у ресторані {restaurant} "
        f'на дату {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
        prices=prices,
        start_parameter=f"create_invoice_rent_place_{number}",
        payload=f"place:{number}:{restaurant}",
        need_email=need_email,
    )
    return await bot.send_invoice(
        call.from_user.id, **place_invoice.generate_invoice()
    )


@dp.callback_query_handler(place_data.filter(choice="no"))
async def deny_offer(call: CallbackQuery, callback_data: dict) -> Message:
    markup = await places_markup(call.message, callback_data["restaurant"])
    message = call.message
    await message.answer(
        "Оберіть вільне місце, яке хочете забронювати", reply_markup=markup
    )
    return await message.reply(
        "Оренда буде дійсна дві години від початку оренди"
    )


@dp.callback_query_handler(text_contains="place")
async def place_callback(call: CallbackQuery) -> Message:
    place = call.data.split(":")[-2]
    restaurant_name = call.data.split(":")[-1]
    markup = place_markup(place, restaurant_name)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = (
        f"Ви впевнені у оренді місця з номером {hbold(place)}?\nОренда буде записана на ім'я: "
        f"{hbold(call.from_user.full_name)}\nПочаток оренди: {hbold(date)}"
    )
    return await call.message.answer(text, reply_markup=markup)
