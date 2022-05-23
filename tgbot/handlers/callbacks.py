from aiogram.types import CallbackQuery, Message, LabeledPrice
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline.places_keyboard import place_markup, places_markup
from tgbot.keyboards.inline.callback_data import place_callback as place_data
from loader import dp, bot

from datetime import datetime

from tgbot.misc.invoices.invoice import Item


@dp.callback_query_handler(text='busy_place')
async def place_callback(call: CallbackQuery) -> Message:
    return await call.message.answer('Це місце зайнято. Оберіть інше.')


@dp.callback_query_handler(place_data.filter(choice='yes'))
async def accept_offer(call: CallbackQuery, callback_data: dict) -> Message:
    number = callback_data['number']
    place_invoice = Item(
        title=f'Місце з номером {number}',
        description=f'Оренда місця з номером {call.data.split(":")[-1]} на дату {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
        currency='UAH',
        prices=[
            LabeledPrice(
                label='Оренда столика',
                amount=10
            )],
        start_parameter=f'create_invoice_rent_place_{number}',
    )
    await bot.send_invoice(call.from_user.id, **place_invoice.generate_invoice(), payload=f'place:{number}')
    return await call.message.reply('Непогано.')


@dp.callback_query_handler(place_data.filter(choice='no'))
async def deny_offer(call: CallbackQuery) -> Message:
    markup = await places_markup(call.message)
    message = call.message
    await message.answer('Оберіть вільне місце, яке хочете забронювати', reply_markup=markup)
    return await message.reply('Оренда буде дійсна дві години від початку оренди')


@dp.callback_query_handler(text_contains='place')
async def place_callback(call: CallbackQuery) -> Message:
    place = call.data.split(":")[-1]
    markup = place_markup(place)
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    text = f'Ви впевнені у оренді місця з номером {hbold(place)}?\nОренда буде записана на ім\'я: ' \
           f'{hbold(call.from_user.full_name)}\nПочаток оренди: {hbold(date)}'
    return await call.message.answer(text, reply_markup=markup)
