from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def subcategories_markup(subcategories: list) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for subcategory in subcategories:
        markup.add(KeyboardButton(subcategory))
    return markup
