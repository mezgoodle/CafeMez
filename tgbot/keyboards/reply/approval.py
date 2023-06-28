from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def approval_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True, row_width=2
    )
    markup.row(KeyboardButton("Так"), KeyboardButton("Ні"))
    return markup
