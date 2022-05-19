from random import random

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_data import place_callback


def create_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=5)
    for place in range(1, 24):
        free = random() > 0.5
        if free:
            place_button = InlineKeyboardButton(text=f"✅{place}",
                                                callback_data=place_callback.new(place))
        else:
            place_button = InlineKeyboardButton(text=f"❌{place}",
                                                callback_data='busy_place')
        markup.insert(place_button)
    return markup
