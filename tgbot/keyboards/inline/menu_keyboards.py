from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_data import menu_callback
from tgbot.misc.backend import Item


def make_callback_data(level, category='0', subcategory='0', item_id='0'):
    return menu_callback.new(level=level, category=category, subcategory=subcategory, item_id=item_id)


async def categories_keyboard(api: Item) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 0
    markup = InlineKeyboardMarkup()

    categories = await api.get_categories()
    for category in categories:
        number_of_items = await api.count_items(category['category_code'])
        button_text = f'{category["category_name"]} ({number_of_items} шт.)'
        callback_data = make_callback_data(level=CURRENT_LEVEL+1, category=category['category_code'])
        markup.insert(InlineKeyboardButton(button_text, callback_data=callback_data))
    return markup