from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery, Message

from tgbot.handlers.menu import list_categories
from loader import dp
from tgbot.keyboards.inline.cart_keyboard import cart_keyboard
from tgbot.keyboards.inline.callback_data import cart_callback
from tgbot.misc.backend import Item
from tgbot.misc.storage import Storage


@dp.message_handler(lambda message: not message.text.isdigit() and int(message.text) <= 0, state='item_amount')
async def item_amount_handler(message: Message):
    return await message.reply(f'Введіть кількість товару у {hbold("цифрах")} та більше нуля')


@dp.message_handler(state='item_amount')
async def item_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    amount = int(message.text)
    storage: Storage = message.bot.get('storage')
    storage.add_to_cart(message.from_user.id, item_id, amount)
    await state.reset_state()
    await message.answer('Ви успішно додали товар до корзини!')
    return await list_categories(message)


@dp.callback_query_handler(cart_callback.filter(action='show'))
async def show_item(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(cart_callback.filter(action='change'))
async def change_amount(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(cart_callback.filter(action='remove'))
async def delete_item(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(text_contains='buy:')
async def apply_purchase(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(text_contains='cancel_cart')
async def cancel_purchase(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.message_handler(Command("cart"))
async def show_cart(message: Message):
    storage: Storage = message.bot.get('storage')
    api: Item = message.bot.get('items_api')
    cart = storage.get_cart(message.from_user.id)
    if not cart:
        return await message.answer('Корзина порожня!')
    text = f'- Щоб побачити продукт, натисніть на його {hbold("назву")}\n' \
           f'- Щоб змінити к-сть, натисніть на {hbold("Змінити")}\n' \
           f'- Щоб видалити зі списку, натисніть на {hbold("Видалити")}\n' \
           f'- Щоб підтвердити чи скасувати замовлення, натисніть {hbold("відповідні кнопки")}\n\n' \
           'Ваша корзина:'
    keyboard = await cart_keyboard(api, cart)
    return await message.answer(text, reply_markup=keyboard)
