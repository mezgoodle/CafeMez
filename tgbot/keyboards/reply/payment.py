from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def payments_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row(KeyboardButton(text="Готівка"), KeyboardButton(text="Картка"))
    return markup
