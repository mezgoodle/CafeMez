from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ContentTypes

from loader import dp
from tgbot.keyboards.inline.support_keyboard import create_keyboard, cancel_support
from tgbot.keyboards.inline.callback_data import support_callback, cancel_support_callback
from tgbot.misc.support import check_support_available, get_support_manager


@dp.message_handler(Command('support_call'))
async def ask_support_call(message: Message) -> Message:
    text = 'Хочете зв\'язатись із оператором техпідтримки? Натисніть кнопку нижче!'
    keyboard = await create_keyboard(messages='many')
    return await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='many', as_user='yes'))
async def send_to_support_call(call: CallbackQuery, state: FSMContext, callback_data: dict) -> Message:
    bot: Bot = call.bot
    await call.message.edit_text('Ви звернулися до техпідтримки! Очікуйте відповідь оператора')
    user_id = int(callback_data.get('user_id'))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id
    if not support_id:
        await state.reset_state()
        return await call.message.edit_text('На жаль, немає доступних операторів для зв\'язку!')
    await state.set_state('wait_in_support')
    await state.update_data(second_id=support_id)

    keyboard = await create_keyboard(messages='many', user_id=call.from_user.id)

    return await bot.send_message(support_id, f'З вами хоче зв\'язатись користувач {call.from_user.full_name}!',
                                  reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='many', as_user='no'))
async def answer_support_call(call: CallbackQuery, state: FSMContext, callback_data: dict) -> Message:
    bot: Bot = call.bot
    second_id = int(callback_data.get('user_id'))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != 'wait_in_support':
        return await call.message.edit_text('На жаль, користувач вже передумав!')

    await state.set_state('in_support')
    await user_state.set_state('in_support')

    await state.update_data(second_id=second_id)

    keyboard = await cancel_support(second_id)
    keyboard_second_user = await cancel_support(call.from_user.id)

    new_message = await call.message.edit_text(
        'Ви на зв\'язку з користувачем!\n Щоб завершити спілкування, натисніть кнопку нижче!',
        reply_markup=keyboard)
    await new_message.pin()
    new_second_message = await bot.send_message(second_id,
                                                'Техпідтримка на зв\'язку з вами! Можете писати сюди ваші повідомлення. \n'
                                                'Щоб закінчити спілкування, натисніть кнопку нижче',
                                                reply_markup=keyboard_second_user)
    await new_second_message.pin()
    return new_second_message


@dp.message_handler(state='wait_in_support', content_types=ContentTypes.ANY)
async def not_supported(message: Message, state: FSMContext) -> Message:
    data = await state.get_data()
    second_id = data.get('second_id')
    keyboard = await cancel_support(second_id)
    return await message.answer('Дочекайтесь відповіді оператора або відміність сеанс!', reply_markup=keyboard)


@dp.callback_query_handler(cancel_support_callback.filter(),
                           state=['in_support', 'wait_in_support', None])
async def exit_support(call: CallbackQuery, state: FSMContext, callback_data: dict) -> Message:
    bot: Bot = call.bot
    user_id = int(callback_data.get('user_id'))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get('second_id')
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(user_id, 'Користувач завершив сеанс техпідтримки!')
    await state.reset_state()
    return await call.message.edit_text('Ви завершили спілкування!')
