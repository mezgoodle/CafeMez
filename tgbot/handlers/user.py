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
from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.misc.backend import User, Item, Order
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


@dp.message_handler(Command('register'))
async def register(message: Message, state: FSMContext) -> Message:
    api: User = message.bot.get('users_api')
    user = await api.get_user(message.from_user.username)
    if 'detail' in user:
        await state.set_state('enter_email')
        return await message.reply('Введіть вашу електронну адресу')
    return await message.reply('Ви вже зареєстровані!')


@dp.message_handler(state='enter_email')
async def enter_email(message: Message, state: FSMContext) -> Message:
    email = message.text
    api: User = message.bot.get('users_api')
    data, status = await api.create_user(message.from_user.username, email, message.from_user.id)
    await state.finish()
    if status == 201:
        return await message.answer('Ви успішно зареєстровані')
    return await message.answer('Виникла помилка при реєстрації. Зверніться до служби підтримки')


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


@dp.message_handler(Command("my_orders"), is_registered=True)
async def show_customer_order(message: Message):
    api: Order = message.bot.get('orders_api')
    orders = await api.get_orders_by_username(message.from_user.username)
    if orders:
        for order in orders:
            text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
            keyboard = orders_keyboard(order)
            await message.answer(text, reply_markup=keyboard)
        return
    return await message.answer('Ви не зробили жодного замовлення')


@dp.message_handler(Command("faq"))
async def show_faq(message: Message):
    return await message.answer(f'{hbold("Як працює система знижок?")}\n\n'
                                f'Чим більше людей роблять покупок карткою, після того, '
                                f'як ввели ваше реферальне посилання, тим більша є ваша знижка.\n'
                                f'Якщо ви тільки ввели реферальне посилання, то ваша знижка - 2%.\n\n'
                                f'{hbold("Чому відрізняється загальна сума замовлення в чеку від тієї, що надає бот?")}\n\n'
                                f'Бот не враховує знижки до суми, то цифра у чеку - {hbold("головна")}.\n\n'
                                f'{hbold("Коли працюють знижки?")}\n\n'
                                f'Знижки працюють тільки, якщо ви оплатили карткою через бота')
