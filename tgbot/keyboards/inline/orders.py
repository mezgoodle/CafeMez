from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.keyboards.inline.callback_data import order_callback


def orders_keyboard(order: dict):
    keyboard = InlineKeyboardMarkup(row_width=4)
    buttons = []
    for order_item in order['items']:
        buttons.append(InlineKeyboardButton(text=f'{order_item["item"]["name"]} - {order_item["quantity"]}',
                                            callback_data=order_callback.new('show', order_item['id'], '')))
    keyboard.row(*buttons)
    buttons = [InlineKeyboardButton(text=f'{"Оплачене" if order["is_paid"] else "Не оплачене"}',
                                    callback_data=order_callback.new('paid', order['id'], not order['is_paid'])),
               InlineKeyboardButton(text=f'{"Готове" if order["is_ready"] else "Не готове"}',
                                    callback_data=order_callback.new('ready', order['id'], not order['is_ready']))]
    if order['shipping_address_longitude']:
        buttons.append(InlineKeyboardButton(text=f'{"Доставлене" if order["is_delivered"] else "Не доставлене"}',
                                            callback_data=order_callback.new('delivered', order['id'],
                                                                             not order['is_delivered'])))
    keyboard.row(*buttons)
    keyboard.add(InlineKeyboardButton(text=f'Сума: {order["total_price"]}', callback_data=f'text'))
    buttons = [InlineKeyboardButton(text=f'Замовник - {order["user"]["username"]}',
                                    url=f'https://t.me/{order["user"]["username"]}')]
    if order['shipping_address_longitude']:
        if order["connected_courier"]:
            buttons.append(InlineKeyboardButton(
                text=f'Кур\'єр - {order["connected_courier"] if order["connected_courier"] else "немає"}',
                url=f'https://t.me/{order["connected_courier"]}')
            )
        else:
            buttons.append(InlineKeyboardButton(
                text=f'Взяти замовлення',
                callback_data=order_callback.new('courier', order['id'], ''))
            )

    keyboard.row(*buttons)
    keyboard.add(InlineKeyboardButton(
        text=f'Видалити замовлення',
        callback_data=order_callback.new('delete', order['id'], '')))

    return keyboard
