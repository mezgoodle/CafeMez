from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.dispatcher.filters import Command, ForwardedMessageFilter
from aiogram.utils.markdown import hitalic, hbold
from aiogram.utils.exceptions import ChatNotFound
from asyncio import sleep

from loader import dp
from tgbot.misc.admin_utils import check_username, start_registration
from tgbot.keyboards.inline.restaurants_keyboard import restaurants_markup
from tgbot.keyboards.inline.places_keyboard import admin_places_markup
from tgbot.keyboards.inline.callback_data import admin_place_callback, order_callback
from tgbot.keyboards.reply.restaurants import restaurants_markup as reply_restaurants_markup
from tgbot.keyboards.reply.location import location_markup
from tgbot.misc.backend import User as UserAPI, Place, Restaurant, Order, Item
from tgbot.misc.staff_actions import show_orders_message, finish_order_action, staff_action
from tgbot.states.states import User, Mailing
from tgbot.misc.stats import make_analysis


@dp.message_handler(Command(['stats']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    api: Item = message.bot.get('items_api')
    data = await api.get_items_from_finished_orders()
    return await make_analysis(data, message)


@dp.message_handler(Command(['orders']), is_admin=True)
async def show_orders(message: Message) -> Message:
    return await show_orders_message(message)


@dp.message_handler(Command(['rs']), is_admin=True)
async def show_restaurants(message: Message) -> Message:
    api: Restaurant = message.bot.get('restaurants_api')
    restaurants = await api.get_all_restaurants()
    keyboard = await restaurants_markup(restaurants)
    text = f'Список ресторанів у базі даних. Щоб видалити, {hbold("натисніть хрестик")} навпроти імені номеру' \
           f' ресторану:\n'
    for index, restaurant in enumerate(restaurants, start=1):
        text += f'{hitalic(index)}. {restaurant["name"]}\n'
    return await message.reply(text, reply_markup=keyboard)


@dp.message_handler(Command(['add_admin']), is_general_admin=True)
async def add_admin(message: Message, state: FSMContext) -> Message:
    await state.update_data(is_courier=False, is_chef=False, is_staff=True)
    return await start_registration(message)


@dp.message_handler(Command(['add_chef']), is_general_admin=True)
async def add_chef(message: Message, state: FSMContext) -> Message:
    await state.update_data(is_chef=True, is_courier=False, is_staff=False)
    return await start_registration(message)


@dp.message_handler(Command(['add_courier']), is_general_admin=True)
async def add_courier(message: Message, state: FSMContext) -> Message:
    await state.update_data(is_courier=True, is_chef=False, is_staff=False)
    return await start_registration(message)


@dp.message_handler(ForwardedMessageFilter(True), state=User.credentials)
async def answer_credentials(message: Message, state: FSMContext) -> Message:
    await User.next()
    try:
        await state.update_data(username=message.forward_from.username, telegram_id=message.forward_from.id)
    except AttributeError:
        return await message.reply(f'{hbold("Перегляньте будь ласка налаштування приватності")}')
    return await message.answer('Введіть пароль')


@dp.message_handler(state=User.password)
async def answer_password(message: Message, state: FSMContext) -> Message:
    await User.next()
    await state.update_data(password=message.text)
    keyboard = await reply_restaurants_markup(message)
    return await message.answer('Виберіть ресторан', reply_markup=keyboard)


@dp.message_handler(state=User.restaurant)
async def answer_restaurant(message: Message, state: FSMContext) -> Message:
    await User.next()
    await state.update_data(restaurant=message.text)
    return await message.answer('Введіть поштовий адрес')


@dp.message_handler(state=User.email)
async def answer_email(message: Message, state: FSMContext) -> Message:
    await state.update_data(email=message.text)
    data = await state.get_data()
    await state.finish()
    api: UserAPI = message.bot.get('users_api')
    _, status = await api.create_user(**data)
    if status == 201 or status == 200:
        await message.answer('Користувача успішно створено')
        return await message.answer(
            f'Username: {hbold(data["username"])}\nPassword: {hbold(data["password"])}\nEmail: {hbold(data["email"])}')
    return await message.reply('Виникла проблема. Зверніться до головного адміністратора')


@dp.message_handler(Command(['remove_admin']), is_general_admin=True)
async def add_admin(message: Message, command: Command.CommandObj) -> Message:
    success, text = check_username(command)
    if success:
        api: UserAPI = message.bot.get('users_api')
        status = await api.delete_user(text)
        if status == 204:
            return await message.reply(f'Користувача {hbold(text)} успішно видалено')
        elif status == 404:
            return await message.reply(f'Користувача {hbold(text)} не знайдено')
        return await message.reply('Виникла проблема. Зверніться до головного адміністратора')
    return await message.reply(text)


@dp.message_handler(Command(['add_rs']), is_admin=True)
async def add_restaurant(message: Message, state: FSMContext) -> Message:
    await state.set_state('cafe_coords')
    markup = location_markup()
    return await message.reply('Надішліть локацію через кнопку або просто як вкладення', reply_markup=markup)


@dp.message_handler(state='cafe_coords',
                    content_types=ContentType.LOCATION, is_admin=True)
async def add_cafe_coords(message: Message, state: FSMContext) -> Message:
    await state.set_state('cafe_name')
    await state.update_data(longitude=message.location.longitude, latitude=message.location.latitude)
    return await message.reply('Напишіть назву ресторану')


@dp.message_handler(state='cafe_name', is_admin=True)
async def answer_cafe_name(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    await state.finish()
    api = message.bot.get('restaurants_api')
    response = await api.create_restaurant(message.text, data['latitude'], data['longitude'])
    if response:
        return await message.answer(f'Дякую! Ресторан {hbold(message.text)} доданий до бази даних.')
    return await message.reply('Щось пішло не так. Зверніться до головного адміністратора.')


@dp.message_handler(Command(['places']), is_admin=True)
async def edit_places(message: Message, state: FSMContext) -> Message:
    markup = await reply_restaurants_markup(message)
    await state.set_state('admin_restaurant_name')
    return await message.answer('Оберіть ресторан, у якому хочете редагувати місце', reply_markup=markup)


@dp.message_handler(state='admin_restaurant_name', is_admin=True)
async def edit_places_in_restaurant(message: Message, state: FSMContext) -> Message:
    restaurant_name = message.text
    keyboard = await admin_places_markup(message, restaurant_name)
    await state.finish()
    return await message.answer('Будь ласка, редагуйте місця за допомогою кнопок', reply_markup=keyboard)


@dp.callback_query_handler(admin_place_callback.filter(method='update'),
                           is_admin=True)
async def update_places_in_restaurant(call: CallbackQuery, callback_data: dict) -> Message:
    api: Place = call.bot.get('places_api')
    _, status = await api.update_place(callback_data['place_id'], {'free': callback_data['value']})
    if status == 200:
        return await call.message.edit_text('Місце успішно оновлено')
    return await call.message.edit_text('Виникла помилка. Зверніться до головного адміністратора')


@dp.callback_query_handler(admin_place_callback.filter(method='remove'),
                           is_admin=True)
async def delete_places_in_restaurant(call: CallbackQuery, callback_data: dict) -> Message:
    api: Place = call.bot.get('places_api')
    status = await api.remove_place(callback_data['place_id'])
    if status == 204:
        return await call.message.edit_text('Місце успішно видалено')
    return await call.message.edit_text('Виникла помилка. Зверніться до головного адміністратора')


@dp.message_handler(Command(['tell_everyone']), is_admin=True)
async def mailing(message: Message):
    await Mailing.first()
    return await message.answer('Надішліть текст повідомлення!')


@dp.message_handler(state=Mailing.text, is_admin=True)
async def enter_text(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await state.reset_state()
    api: UserAPI = message.bot.get('users_api')
    bot = message.bot
    users = await api.get_all_users()
    for user in users:
        try:
            await bot.send_message(user['telegram_id'], text)
            await sleep(0.3)
        except ChatNotFound:
            pass
    return await message.answer('Повідомлення надіслано!')


@dp.callback_query_handler(order_callback.filter(action='finished'),
                           is_admin=True)
async def finish_order(callback_query: CallbackQuery, callback_data: dict):
    return await finish_order_action(callback_query, callback_data, 'Статус замовлення змінено!',
                                     'Помилка при зміні статусу замовлення!')


@dp.callback_query_handler(order_callback.filter(action='paid'), is_admin=True)
async def change_order_payment(callback_query: CallbackQuery, callback_data: dict):
    return await staff_action(callback_query, callback_data, {'is_paid': callback_data['value']},
                              'Статус оплати змінено!', 'Помилка при зміні статусу оплати!')


@dp.callback_query_handler(order_callback.filter(action='delete'),
                           is_admin=True)
async def delete_order(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get('orders_api')
    status = await api.delete_order(callback_data['id'])
    if status == 204:
        await callback_query.message.delete()
        return await callback_query.message.answer('Замовлення успішно видалено!')
    return await callback_query.message.answer('Помилка при видалення замовлення!')
