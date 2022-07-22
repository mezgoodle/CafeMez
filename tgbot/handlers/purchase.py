from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery, Message

from tgbot.handlers.menu import list_categories
from loader import dp
from tgbot.misc.storage import Storage


@dp.message_handler(lambda message: not message.text.isdigit(), state='item_amount')
async def item_amount_handler(message: Message):
    return await message.reply(f'Введіть кількість товару у {hbold("цифрах")}')


@dp.message_handler(state='item_amount')
async def item_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    item_id = data.get('item_id')
    amount = int(message.text)
    storage: Storage = message.bot.get('storage')
    storage.add_to_cart(message.from_user.id, item_id, amount)
    await state.reset_state()
    await message.answer('Ви успішно додали товар до корзини!')
    return await list_categories(message)


@dp.message_handler(Command("cart"))
async def show_cart(message: Message):
    storage: Storage = message.bot.get('storage')
    cart = storage.get_cart(message.from_user.id)
    if not cart:
        return await message.answer('Корзина порожня!')
    text = 'Ваша корзина:\n'
    for item in cart:
        text += f'{item}\n'
    await message.answer(text)
