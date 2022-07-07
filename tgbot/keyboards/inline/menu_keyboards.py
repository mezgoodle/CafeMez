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
        number_of_items = await api.count_items(category['code'])
        button_text = f'{category["name"]} ({number_of_items} шт.)'
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category['code'])
        markup.insert(InlineKeyboardButton(button_text, callback_data=callback_data))
    return markup


async def subcategories_keyboard(api: Item, category: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 1
    markup = InlineKeyboardMarkup()

    subcategories = await api.get_subcategories(category)
    for subcategory in subcategories:
        number_of_items = await api.count_items(category, subcategory['code'])
        button_text = f'{subcategory["name"]} ({number_of_items} шт.)'
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category,
                                           subcategory=subcategory['code'])
        markup.insert(InlineKeyboardButton(button_text, callback_data=callback_data))
    markup.row(InlineKeyboardButton('Назад', callback_data=make_callback_data(level=CURRENT_LEVEL - 1)))
    return markup


async def items_keyboard(api: Item, category: str, subcategory: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)

    items = await api.get_items(subcategory)
    for item in items:
        button_text = f'{item["name"]} ({item["price"]} гривень.)'
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category,
                                           subcategory=subcategory, item_id=item['id'])
        markup.insert(InlineKeyboardButton(button_text, callback_data=callback_data))
    markup.row(
        InlineKeyboardButton('Назад', callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category)))
    return markup


async def item_keyboard(api: Item, category: str, subcategory: str, item_id: str) -> InlineKeyboardMarkup:
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()

    item = await api.get_item(item_id)
    button_text = f'Додати {item["name"]} ({item["price"]} гривень) до корзини'
    callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=item['subcategory']['category']['code'],
                                       subcategory=item['subcategory']['code'], item_id=item['id'])
    markup.insert(InlineKeyboardButton(button_text, callback_data=callback_data))
    markup.row(InlineKeyboardButton('Назад',
                                    callback_data=make_callback_data(level=CURRENT_LEVEL - 1, category=category,
                                                                     subcategory=subcategory)))
    return markup
