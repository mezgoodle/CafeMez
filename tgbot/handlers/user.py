from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.keyboards.reply.location import location_markup
from tgbot.keyboards.reply.restaurants import restaurants_markup
from tgbot.keyboards.inline.places_keyboard import places_markup
from tgbot.keyboards.inline.cart_keyboard import cart_keyboard
from tgbot.misc.backend import User, Item
from tgbot.misc.storage import Storage


@dp.message_handler(Command(['rs', 'admin_rs']))
async def find_restaurants(message: Message) -> Message:
    markup = location_markup()
    return await message.answer('Надішліть локацію через кнопку або просто як вкладення', reply_markup=markup)


@dp.message_handler(Command(['places', 'admin_places']))
async def show_restaurants(message: Message, state: FSMContext) -> Message:
    markup = await restaurants_markup(message)
    await state.set_state('restaurant_name')
    return await message.answer('Оберіть ресторан, у якому хочете забронювати місце', reply_markup=markup)


@dp.message_handler(state='restaurant_name')
async def show_places(message: Message, state: FSMContext) -> Message:
    restaurant_name = message.text
    await state.finish()
    markup = await places_markup(message, restaurant_name)
    await message.answer('Оберіть вільне місце, яке хочете забронювати', reply_markup=markup)
    return await message.reply('Оренда буде дійсна дві години від початку оренди')


@dp.message_handler(Command(['my_ref']))
async def show_my_ref(message: Message) -> Message:
    api: User = message.bot.get('users_api')
    user = await api.get_user(message.from_user.username)
    if user:
        link = await get_start_link(payload=message.from_user.id)
        return await message.answer(f'Вашe посилання: {link}')
    return await message.answer('Ви не зареєстровані в системі. Для цього введіть команду /register')


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


@dp.message_handler(Command("my_orders"), is_chef=True)
@dp.message_handler(Command("my_orders"), is_courier=True)
async def show_orders(message: Message):
    api: User = message.bot.get('users_api')
    orders = await api.get_orders(message.from_user.username)
    return await message.answer(f'Ваші замовлення:\n{orders}')
