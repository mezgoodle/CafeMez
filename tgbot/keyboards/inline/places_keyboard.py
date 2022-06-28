from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import place_callback


async def places_markup(message: Message, restaurant_name: str) -> InlineKeyboardMarkup:
    api = message.bot.get('places_api')
    places = await api.get_all_places()
    filtered_places = list(filter(lambda place: place['restaurant'] == restaurant_name, places))
    markup = InlineKeyboardMarkup(row_width=5)
    for place in filtered_places:
        if place['free']:
            place_button = InlineKeyboardButton(text=f"✅{place['id']}",
                                                callback_data=f"place:{place['id']}")
        else:
            place_button = InlineKeyboardButton(text=f"❌{place['id']}",
                                                callback_data='busy_place')
        markup.insert(place_button)
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
