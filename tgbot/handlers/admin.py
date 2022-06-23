from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hitalic, hbold

from loader import dp
from tgbot.misc.admin_utils import check_nickname
from tgbot.keyboards.inline.restaurants_keyboard import restaurants_markup
from tgbot.keyboards.reply.location import location_markup


# TODO: make rights for admin and general admin
@dp.message_handler(Command(['stats']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    return await message.reply(f'Hello, {message.from_user.username}!')


@dp.message_handler(Command(['rs']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    api = message.bot.get('restaurants_api')
    restaurants = await api.get_all_restaurants()
    keyboard = await restaurants_markup(restaurants)
    text = f'Список ресторанів у базі даних. Щоб видалити, {hbold("натисніть хрестик")} навпроти імені номеру' \
           f' ресторану:\n'
    for index, restaurant in enumerate(restaurants, start=1):
        text += f'{hitalic(index)}. {restaurant["name"]}\n'
    return await message.reply(text, reply_markup=keyboard)


@dp.message_handler(Command(['add_admin']), is_general_admin=True)
async def add_admin(message: Message, command: Command.CommandObj) -> Message:
    success, text = check_nickname(command)
    if success:
        # TODO: send request to server
        return await message.reply(text)
    return await message.reply(text)


@dp.message_handler(Command(['remove_admin']), is_general_admin=True)
async def add_admin(message: Message, command: Command.CommandObj) -> Message:
    success, text = check_nickname(command, False)
    if success:
        # TODO: send request to server
        return await message.reply(text)
    return await message.reply(text)


@dp.message_handler(Command(['add_rs']), is_general_admin=True)
async def add_restaurant(message: Message, state: FSMContext) -> Message:
    await state.set_state('cafe_coords')
    markup = location_markup()
    return await message.reply('Надішліть локацію через кнопку або просто як вкладення', reply_markup=markup)


@dp.message_handler(state='cafe_coords', content_types=ContentType.LOCATION, is_general_admin=True)
async def add_cafe_coords(message: Message, state: FSMContext) -> Message:
    await state.set_state('cafe_name')
    await state.update_data(longitude=message.location.longitude, latitude=message.location.latitude)
    return await message.reply('Напишіть назву ресторану')


@dp.message_handler(state='cafe_name', is_general_admin=True)
async def answer_cafe_name(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    await state.finish()
    api = message.bot.get('restaurants_api')
    response = await api.create_restaurant(message.text, data['latitude'], data['longitude'])
    if response:
        return await message.answer(f'Дякую! Ресторан {hbold(message.text)} доданий до бази даних.')
    return await message.reply('Щось пішло не так. Зверніться до головного адміністратора.')
