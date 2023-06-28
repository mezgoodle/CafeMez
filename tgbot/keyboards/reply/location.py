from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def location_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Надіслати локацію", request_location=True))
    return markup
