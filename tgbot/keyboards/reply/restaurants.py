from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

from tgbot.misc.backend import Restaurant


async def restaurants_markup(message: Message) -> ReplyKeyboardMarkup:
    api: Restaurant = message.bot.get("restaurants_api")
    restaurants = await api.get_all_restaurants()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for restaurant in restaurants:
        button = KeyboardButton(text=restaurant["name"])
        markup.add(button)
    return markup
