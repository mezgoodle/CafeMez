from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_data import order_callback


def orders_keyboard(order):
    keyboard = InlineKeyboardMarkup(row_width=4)
    buttons = []
    for item in order['items']:
        buttons.append(InlineKeyboardButton(text=f'{item["item"]} - {item["quantity"]}',
                                            callback_data=order_callback.new('show', item['id'], '')))
    keyboard.row(*buttons)
    keyboard.row(
        InlineKeyboardButton(text=f'{"Оплачене" if order["is_paid"] else "Не оплачене"}',
                             callback_data=order_callback.new('paid', order['id'], not order['is_paid'])),
        InlineKeyboardButton(text=f'{"Готове" if order["is_ready"] else "Не готове"}',
                             callback_data=order_callback.new('ready', order['id'], not order['is_ready'])),
    )
    keyboard.add(InlineKeyboardButton(text=f'Сума: {order["total_price"]}', callback_data=f'text'))
    keyboard.row(
        InlineKeyboardButton(text=f'Замовник - {order["user"]}', url=f'https://t.me/{order["user"]}'),
        InlineKeyboardButton(
            text=f'Кур\'єр - {order["connected_courier"] if order["connected_courier"] else "немає"}',
            url=f'https://t.me/{order["connected_courier"]}'),

    )
    keyboard.add(InlineKeyboardButton(
        text=f'Видалити замовлення',
        callback_data=order_callback.new('delete', order['id'], '')))

    return keyboard
