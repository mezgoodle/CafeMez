from aiogram.types import CallbackQuery, Message, LabeledPrice
from aiogram.utils.markdown import hbold, hitalic

from tgbot.keyboards.inline.places_keyboard import place_markup, places_markup
from tgbot.keyboards.inline.restaurants_keyboard import restaurants_markup
from tgbot.keyboards.inline.callback_data import place_callback as place_data
from loader import dp, bot

from datetime import datetime

from tgbot.misc.invoices.invoice import Item


@dp.callback_query_handler(text='busy_place')
async def place_callback(call: CallbackQuery) -> Message:
    return await call.message.answer('Це місце зайнято. Оберіть інше.')


@dp.callback_query_handler(text_contains='rs:')
async def place_callback(call: CallbackQuery) -> Message:
    restaurant_id = call.data.split(':')[1]
    api = call.bot.get('api')
    status = await api.delete(f'restaurants/{restaurant_id}')
    if status == 204:
        restaurants = await api.get('restaurants')
        keyboard = await restaurants_markup(restaurants)
        text = f'Список ресторанів у базі даних. Щоб видалити, {hbold("натисніть хрестик")} навпроти імені номеру' \
               f' ресторану:\n'
        for index, restaurant in enumerate(restaurants, start=1):
            text += f'{hitalic(index)}. {restaurant["name"]}\n'
        await call.message.edit_text(text, reply_markup=keyboard)
        return await call.message.answer('Ресторан було видалено з бази даних.')
    return await call.message.answer('Помилка при видаленні ресторану.')


@dp.callback_query_handler(place_data.filter(choice='yes'))
async def accept_offer(call: CallbackQuery, callback_data: dict) -> Message:
    number = callback_data['number']
    place_invoice = Item(
        title=f'Місце з номером {number}',
        description=f'Оренда місця з номером {number} на дату {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
        prices=[
            LabeledPrice(
                label='Оренда столика',
                amount=100_00
            )],
        start_parameter=f'create_invoice_rent_place_{number}',
        payload=f'place:{number}'
    )
    return await bot.send_invoice(call.from_user.id, **place_invoice.generate_invoice())


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
