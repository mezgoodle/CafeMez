from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ContentTypes

from loader import dp
from tgbot.keyboards.inline.support_keyboard import create_keyboard
from tgbot.keyboards.inline.callback_data import support_callback


@dp.message_handler(Command('support'))
async def ask_support(message: Message) -> Message:
    text = 'Виникла проблема? Натисніть кнопку нижче!'
    keyboard = await create_keyboard(messages='one')
    return await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='one'))
async def send_to_support(call: CallbackQuery, state: FSMContext, callback_data: dict) -> Message:
    user_id = int(callback_data.get('user_id'))
    await state.set_state('wait_for_support_message')
    await state.update_data(second_id=user_id)
    return await call.message.answer('Надішліть ваше повідомлення, яким ви хочете поділитись')


@dp.message_handler(state='wait_for_support_message', content_types=ContentTypes.ANY)
async def get_support_message(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    second_id = data['second_id']
    await state.finish()
    bot: Bot = message.bot
    await bot.send_message(second_id, f'Вам надійшов лист! Щоб відповісти, натисніть кнопку нижче!')
    keyboard = await create_keyboard(messages='one', user_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=keyboard)
    await state.reset_state()
    return await message.answer('Ви надіслали це повідомлення!')
