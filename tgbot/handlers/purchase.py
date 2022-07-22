from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.types import CallbackQuery, Message

from tgbot.handlers.menu import list_categories
from loader import dp
from tgbot.misc.storage import Storage


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
