from typing import Union

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from loader import dp
from tgbot.keyboards.inline.callback_data import menu_callback
from tgbot.keyboards.inline.menu_keyboards import (
    categories_keyboard,
    subcategories_keyboard,
    items_keyboard,
    item_keyboard,
)


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await list_categories(message)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    markup = await categories_keyboard(message.bot.get("items_api"))
    if isinstance(message, Message):
        await message.answer("Дивись, що у нас є", reply_markup=markup)
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.edit_text("Дивись, що у нас є", reply_markup=markup)


async def list_subcategories(callback: CallbackQuery, category: str, **kwargs):
    markup = await subcategories_keyboard(callback.bot.get("items_api"), category)
    await callback.message.edit_reply_markup(markup)


async def list_items(
    callback: CallbackQuery, category: str, subcategory: str, **kwargs
):
    markup = await items_keyboard(callback.bot.get("items_api"), category, subcategory)
    await callback.message.edit_text(text="Дивись, що у нас є", reply_markup=markup)


async def show_item(
    callback: CallbackQuery, category: str, subcategory: str, item_id: str, **kwargs
):
    api = callback.bot.get("items_api")
    markup = await item_keyboard(api, category, subcategory, item_id)
    item = await api.get_item(item_id)
    text = f'Купити {item["name"]} ({item["price"]} гривень.)'
    await callback.message.edit_text(text=text, reply_markup=markup)


async def buy_item(callback: CallbackQuery, item_id: str, state: FSMContext, **kwargs):
    await state.update_data(item_id=item_id)
    await state.set_state("item_amount")
    return await callback.message.answer("Введіть кількість товару(у цифрах):")


@dp.callback_query_handler(menu_callback.filter())
async def menu_navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    current_level = callback_data.get("level")
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")
    item_id = callback_data.get("item_id")

    levels = {
        "0": list_categories,
        "1": list_subcategories,
        "2": list_items,
        "3": show_item,
        "4": buy_item,
    }
    current_level_function = levels.get(current_level)

    await current_level_function(
        call, category=category, subcategory=subcategory, item_id=item_id, state=state
    )
