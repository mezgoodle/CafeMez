from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from tgbot.keyboards.inline.callback_data import rs_callback


async def restaurants_markup(restaurants: list) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=4)
    for index, restaurant in enumerate(restaurants, start=1):
        cancel_button = InlineKeyboardButton(
            text=f"{index}❌", callback_data=rs_callback.new(number=restaurant["name"])
        )
        markup.insert(cancel_button)
    return markup
