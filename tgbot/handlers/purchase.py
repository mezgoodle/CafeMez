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


@dp.message_handler(lambda message: not message.text.isdigit() and int(message.text) <= 0,
                    state=['item_amount', 'change_amount'])
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


@dp.message_handler(state='change_amount')
async def change_item_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    amount = int(message.text)
    storage: Storage = message.bot.get('storage')
    storage.change_amount(message.from_user.id, item_id, amount)
    cart = storage.get_cart(message.from_user.id)
    await state.reset_state()
    await message.answer('Ви успішно змінили кількість товару!')
    api: Item = message.bot.get('items_api')
    keyboard = await cart_keyboard(api, cart)
    return await message.answer('Ваша оновлена корзина:', reply_markup=keyboard)


@dp.callback_query_handler(cart_callback.filter(action='show'))
async def show_item(callback_query: CallbackQuery, callback_data: dict):
    item_id = callback_data['item_id']
    api: Item = callback_query.bot.get('items_api')
    item = await api.get_item(item_id)
    return await callback_query.message.answer(f'{item["name"]} - {item["price"]} грн')


@dp.callback_query_handler(cart_callback.filter(action='change'))
async def change_amount(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    item_id = callback_data['item_id']
    await state.update_data(item_id=item_id)
    await state.set_state('change_amount')
    return await callback_query.message.answer('Введіть нову кількість товару')


@dp.callback_query_handler(cart_callback.filter(action='remove'))
async def delete_item(callback_query: CallbackQuery, callback_data: dict):
    item_id = callback_data['item_id']
    storage: Storage = callback_query.bot.get('storage')
    storage.remove_from_cart(callback_query.from_user.id, item_id)
    cart = storage.get_cart(callback_query.from_user.id)
    await callback_query.message.answer('Ви видалили товар з корзини!')
    if cart:
        api: Item = callback_query.bot.get('items_api')
        keyboard = await cart_keyboard(api, cart)
        return await callback_query.message.answer('Ваша оновлена корзина:', reply_markup=keyboard)


@dp.callback_query_handler(text_contains='buy:')
async def apply_purchase(callback_query: CallbackQuery, callback_data: dict):
    pass


@dp.callback_query_handler(text_contains='cancel_cart')
async def cancel_purchase(callback_query: CallbackQuery, *args, **kwargs):
    storage: Storage = callback_query.bot.get('storage')
    storage.clean_cart(callback_query.from_user.id)
    await callback_query.message.answer('Ви відмінили покупку!')
    return await list_categories(callback_query.message)


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
