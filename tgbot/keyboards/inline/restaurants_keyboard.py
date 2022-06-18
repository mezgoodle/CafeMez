from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import rs_callback


async def restaurants_markup(restaurants: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    for restaurant in restaurants:
        cancel_button = InlineKeyboardButton(text=f"{restaurant['id']}❌",
                                             callback_data=rs_callback.new(number=restaurant['id']))
        markup.insert(cancel_button)
    return markup
