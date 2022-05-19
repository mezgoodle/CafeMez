from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline.places_keyboard import place_markup, places_markup
from tgbot.keyboards.inline.callback_data import place_callback as place_data
from loader import dp

from datetime import datetime


@dp.callback_query_handler(text='busy_place')
async def place_callback(call: CallbackQuery) -> Message:
    return await call.answer('Це місце зайнято. Оберіть інше.', show_alert=True)


@dp.callback_query_handler(place_data.filter(choice='yes'))
async def accept_offer(call: CallbackQuery) -> Message:
    return await call.answer('Непогано.', show_alert=True)


@dp.callback_query_handler(place_data.filter(choice='no'))
async def deny_offer(call: CallbackQuery) -> Message:
    markup = places_markup()
    message = call.message
    await message.answer('Оберіть вільне місце, яке хочете забронювати', reply_markup=markup)
    return await message.reply('Оренда буде дійсна дві години від початку оренди')


@dp.callback_query_handler(text_contains='place')
async def place_callback(call: CallbackQuery) -> Message:
    await call.answer()
    place = call.data.split(":")[-1]
    markup = place_markup(place)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'Ви впевнені у оренді місця з номером {hbold(place)}?\nОренда буде записана на ім\'я: ' \
           f'{hbold(call.from_user.full_name)}\nПочаток оренди: {hbold(date)}'
    return await call.message.answer(text, reply_markup=markup)
