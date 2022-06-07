from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import place_callback


async def restaurants_markup(message: Message) -> InlineKeyboardMarkup:
    api = message.bot.get('api')
    restaurants = await api.get('restaurants')
    markup = InlineKeyboardMarkup(row_width=2)
    for restaurant in restaurants:
        restaurant_button = InlineKeyboardButton(text=restaurant['name'], callback_data='none')
        cancel_button = InlineKeyboardButton(text="❌", callback_data='delete_rs')
        markup.add(restaurant_button, cancel_button)
        # markup.insert(restaurant_button)
    return markup
