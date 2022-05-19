from aiogram.types import CallbackQuery, Message

from loader import dp


@dp.callback_query_handler(text='busy_place')
async def place_callback(call: CallbackQuery) -> Message:
    return await call.answer('Це місце зайнято. Оберіть інше.', show_alert=True)


@dp.callback_query_handler(text_contains='place')
async def place_callback(call: CallbackQuery) -> Message:
    await call.answer()
    place = call.data.split(":")[-1]
    return await call.message.answer(place)
