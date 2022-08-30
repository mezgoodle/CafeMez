from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from tgbot.keyboards.inline.callback_data import place_callback, admin_place_callback


async def places_markup(message: Message, restaurant_name: str) -> InlineKeyboardMarkup:
    api = message.bot.get('places_api')
    places = await api.get_places_by_restaurant(restaurant_name)
    markup = InlineKeyboardMarkup(row_width=5)
    for index, place in enumerate(places, start=1):
        if place['free']:
            place_button = InlineKeyboardButton(text=f"✅{index}",
                                                callback_data=f"place:{place['id']}:{restaurant_name}")
        else:
            place_button = InlineKeyboardButton(text=f"❌{index}",
                                                callback_data='busy_place')
        markup.insert(place_button)
    return markup


async def admin_places_markup(message: Message, restaurant_name: str) -> InlineKeyboardMarkup:
    api = message.bot.get('places_api')
    places = await api.get_places_by_restaurant(restaurant_name)
    markup = InlineKeyboardMarkup(row_width=3)
    for index, place in enumerate(places, start=1):
        number_button = InlineKeyboardButton(text=f"Місце #{index}", callback_data='nothing')
        place_button = InlineKeyboardButton(
            text=f"Змінити на {'зайняте' if place['free'] else 'вільне'}",
            callback_data=admin_place_callback.new('update', place['id'], not place['free'])
        )
        remove_button = InlineKeyboardButton(
            text='Видалити',
            callback_data=admin_place_callback.new('remove', place['id'], '')
        )
        markup.row(number_button, place_button, remove_button)
    return markup


def place_markup(number: str, restaurant_name: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)
    place_button = InlineKeyboardButton(text=f"✅Орендувати",
                                        callback_data=place_callback.new(number=number, choice='yes',
                                                                         restaurant=restaurant_name))
    markup.insert(place_button)
    place_button = InlineKeyboardButton(text=f"❌Обрати інше",
                                        callback_data=place_callback.new(number=number, choice='no',
                                                                         restaurant=restaurant_name))
    markup.insert(place_button)
    return markup
