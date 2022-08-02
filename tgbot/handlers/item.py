from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.states.states import Item
from tgbot.keyboards.reply.subcategories import subcategories_markup
from tgbot.misc.backend import Item as ItemBackend


# TODO: add approval as final state step
@dp.message_handler(Command("add_item"), is_admin=True)
async def add_item(message: Message):
    await Item.first()
    return await message.reply("Напишіть назву товару")


@dp.message_handler(state=Item.name)
async def answer_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await Item.next()
    return await message.reply("Напишіть ціну товару")


@dp.message_handler(state=Item.price)
async def answer_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await Item.next()
    return await message.reply("Напишіть опис товару")


@dp.message_handler(state=Item.description)
async def answer_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await Item.next()
    return await message.reply(
        f"Надішліть фото товару. {hbold('Надсилати фото у вигляді картинки. Формат файлу не приймається')}")


@dp.message_handler(state=Item.photo, content_types=ContentType.PHOTO)
async def answer_photo(message: Message, state: FSMContext, subcategories: list):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await Item.next()
    keyboard = await subcategories_markup(subcategories)
    return await message.reply("Оберіть категорію товару", reply_markup=keyboard)


@dp.message_handler(state=Item.subcategory)
async def answer_subcategory(message: Message, state: FSMContext, subcategories: list):
    subcategory = message.text
    if not subcategory in subcategories:
        return await message.reply("Оберіть категорію товару із клавіатури")
    api: ItemBackend = message.bot.get('items_api')
    await state.update_data(subcategory=subcategory)
    data = await state.get_data()
    await state.finish()
    _, status = await api.create_item(data)
    if status == 201:
        return await message.reply(f'Товар "{data["name"]}" був створений')
    return await message.reply('f')
