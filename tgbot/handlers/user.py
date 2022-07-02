from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from loader import dp
from tgbot.keyboards.reply.location import location_markup
from tgbot.keyboards.reply.restaurants import restaurants_markup
from tgbot.keyboards.inline.places_keyboard import places_markup


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
    link = await get_start_link(payload=message.from_user.id)
    return await message.answer(f'Вашe посилання: {link}')
