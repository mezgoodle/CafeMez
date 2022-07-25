from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_data import cart_callback
from tgbot.misc.backend import Item

from collections import Counter


async def cart_keyboard(api: Item, items_ids: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    total_price = 0
    cart_items = Counter(items_ids)
    for item_id, amount in cart_items.items():
        item = await api.get_item(item_id)
        total_price += float(item['price']) * amount
        keyboard.row(InlineKeyboardButton(text=f'{item["name"]}, {amount} шт.',
                                           callback_data=cart_callback.new('show', item_id)),
                     InlineKeyboardButton(text='Видалити',
                                           callback_data=cart_callback.new('remove', item_id)),
                     InlineKeyboardButton(text='Змінити',
                                           callback_data=cart_callback.new('change', item_id)))
    keyboard.add(InlineKeyboardButton(text=f'Всього: {total_price} грн', callback_data='nothing'))
    keyboard.add(InlineKeyboardButton(text='Підтвердити', callback_data=f'buy:{total_price}'))
    keyboard.add(InlineKeyboardButton(text='Відмінити', callback_data='cancel_cart'))
    return keyboard
