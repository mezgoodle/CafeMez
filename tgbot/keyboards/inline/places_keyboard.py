from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import place_callback


async def places_markup(message: Message, restaurant_name: str) -> InlineKeyboardMarkup:
    api = message.bot.get('places_api')
    places = await api.get_places_by_restaurant(restaurant_name)
    markup = InlineKeyboardMarkup(row_width=5)
    for place in places:
        if place['free']:
            place_button = InlineKeyboardButton(text=f"✅{place['id']}",
                                                callback_data=f"place:{place['id']}")
        else:
            place_button = InlineKeyboardButton(text=f"❌{place['id']}",
                                                callback_data='busy_place')
        markup.insert(place_button)
    return markup


async def admin_places_markup(message: Message, restaurant_name: str) -> InlineKeyboardMarkup:
    api = message.bot.get('places_api')
    places = await api.get_places_by_restaurant(restaurant_name)
    markup = InlineKeyboardMarkup(row_width=3)
    for place in places:
        number_button = InlineKeyboardButton(text=f"Місце #{place['id']}", callback_data='nothing')
        place_button = InlineKeyboardButton(
            text=f"Змінити на Вільне",
            callback_data=f"edit_place:{place['id']}"
        )
        remove_button = InlineKeyboardButton(
            text='Видалити',
            callback_data=f"remove_place:{place['id']}"
        )
        markup.row(number_button, place_button, remove_button)
    return markup


def place_markup(number: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    place_button = InlineKeyboardButton(text=f"✅Орендувати",
                                        callback_data=place_callback.new(number=number, choice='yes'))
    markup.insert(place_button)
    place_button = InlineKeyboardButton(text=f"❌Обрати інше",
                                        callback_data=place_callback.new(number=number, choice='no'))
    markup.insert(place_button)
    return markup
