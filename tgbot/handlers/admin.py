from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hitalic, hbold

from loader import dp
from tgbot.misc.admin_utils import check_nickname


# TODO: make rights for admin and general admin
@dp.message_handler(Command(['stats']), is_general_admin=True)
async def show_stats(message: Message) -> Message:
    return await message.reply(f'Hello, {message.from_user.username}!')


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


@dp.message_handler(content_types=ContentType.LOCATION, is_general_admin=True)
async def add_cafe_coords(message: Message, state: FSMContext) -> Message:
    # TODO: send request to server
    await state.set_state('cafe_name')
    await state.update_data(longitude=message.location.longitude, latitude=message.location.latitude)
    return await message.reply('Напишіть назву ресторану')


@dp.message_handler(state='cafe_name', is_general_admin=True)
async def answer_cafe_name(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    await state.finish()
    api = message.bot.get('api')
    response_code = await api.post('restaurants',
                          {'name': message.text, 'latitude': data['latitude'], 'longitude': data['longitude']})
    if response_code == 201:
        return await message.answer(f'Дякую! Ресторан {hbold(message.text)} доданий до бази даних.')
    return await message.reply('Щось пішло не так. Зверніться до головного адміністратора.')
