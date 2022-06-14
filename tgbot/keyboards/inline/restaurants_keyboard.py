from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import place_callback


async def restaurants_markup(restaurants: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    for restaurant in restaurants:
        cancel_button = InlineKeyboardButton(text=f"{restaurant['id']}❌", callback_data='delete_rs')
        markup.insert(cancel_button)
    return markup
