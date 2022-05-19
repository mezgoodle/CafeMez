from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline.places_keyboard import place_markup
from loader import dp

from datetime import datetime


@dp.callback_query_handler(text='busy_place')
async def place_callback(call: CallbackQuery) -> Message:
    return await call.answer('Це місце зайнято. Оберіть інше.', show_alert=True)


@dp.callback_query_handler(text_contains='place')
async def place_callback(call: CallbackQuery) -> Message:
    await call.answer()
    place = call.data.split(":")[-1]
    markup = place_markup(place)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'Ви впевнені у оренді місця з номером {hbold(place)}?\nОренда буде записана на ім\'я: ' \
           f'{hbold(call.from_user.full_name)}\nПочаток оренди: {hbold(date)}'
    return await call.message.answer(text, reply_markup=markup)
