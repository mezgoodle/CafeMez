from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ContentType

from tgbot.handlers.menu import list_categories
from loader import dp
from tgbot.keyboards.inline.cart_keyboard import cart_keyboard
from tgbot.keyboards.inline.callback_data import cart_callback
from tgbot.keyboards.reply.restaurants import restaurants_markup
from tgbot.keyboards.reply.payment import payments_markup
from tgbot.misc.backend import Item, Restaurant, Order
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


@dp.callback_query_handler(text_contains='cancel_cart')
async def cancel_purchase(callback_query: CallbackQuery):
    storage: Storage = callback_query.bot.get('storage')
    storage.clean_cart(callback_query.from_user.id)
    await callback_query.message.answer('Ви відмінили покупку!')
    return await list_categories(callback_query.message)


@dp.callback_query_handler(text_contains='buy:')
async def apply_purchase(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state('shipping_address')
    keyboard = await restaurants_markup(callback_query.message)
    text = 'Чи бажаєте ви доставку замовлення?' \
           f'\nЯкщо {hbold("так")}, надішліть координати доставки.' \
           f'\nЯкщо {hbold("ні")}, виберіть один із ресторанів'
    return await callback_query.message.answer(text, reply_markup=keyboard)


@dp.message_handler(state='shipping_address', content_types=ContentType.TEXT)
async def shipping_address_as_text(message: Message, state: FSMContext):
    restaurant_name = message.text
    api: Restaurant = message.bot.get('restaurants_api')
    restaurant = await api.get_restaurant(restaurant_name)
    if name := restaurant['name']:
        await state.update_data(restaurant_name=name, shipping_price=None, longitude=None, latitude=None)
        await state.set_state('payment_method')
        keyboard = payments_markup()
        return await message.answer('Виберіть спосіб оплати', reply_markup=keyboard)


@dp.message_handler(state='shipping_address', content_types=ContentType.LOCATION)
async def shipping_address_as_location(message: Message, state: FSMContext):
    restaurant_location = message.location
    api: Order = message.bot.get('orders_api')
    restaurant_name, shipping_price = await api.get_shipping_price(restaurant_location, message.bot)
    await state.update_data(shipping_price=shipping_price, restaurant_name=restaurant_name,
                            longitude=restaurant_location.longitude, latitude=restaurant_location.latitude)
    await state.set_state('payment_method')
    keyboard = payments_markup()
    return await message.answer('Виберіть спосіб оплати', reply_markup=keyboard)


@dp.message_handler(Text(equals=['Картка', 'Готівка'], ignore_case=True), state='payment_method', )
async def answer_payment_method(message: Message, state: FSMContext):
    await state.update_data(payment_method=message.text)
    data = await state.get_data()
    api: Order = message.bot.get('orders_api')
    payment_dict = {'Картка': 'CD', 'Готівка': 'CH'}
    order, status = await api.create_order(user=message.from_user.username,
                                           payment_method=payment_dict[message.text],
                                           shipping_address_longitude=float(data['longitude']),
                                           shipping_address_latitude=float(data['latitude']),
                                           shipping_address_name=data['restaurant_name'],
                                           shipping_price=data['shipping_price'],
                                           )
    print(order, status)
    return await message.answer('Ви обрали спосіб оплати: ' + message.text)
