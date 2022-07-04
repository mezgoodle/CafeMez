from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.misc.support import get_support_manager
from tgbot.config import load_config, Config
from tgbot.keyboards.inline.callback_data import support_callback, cancel_support_callback

from random import choice


async def create_keyboard(messages, user_id=None):
    config: Config = load_config()
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Відповісти користувачу'
    else:
        contact_id = await get_support_manager()
        as_user = 'yes'
        if messages == 'many' and contact_id is None:
            return False
        elif messages == 'one' and contact_id is None:
            contact_id = choice(config.tg_bot.admins)
        if messages == 'one':
            text = 'Написати одне повідомлення у техпідтримку'
        else:
            text = 'Написати оператору'
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text=text,
                                      callback_data=support_callback.new(
                                          messages=messages,
                                          user_id=contact_id,
                                          as_user=as_user)
                                      )
                 )
    if messages == 'many':
        keyboard.add(InlineKeyboardButton(text='Закінчити сеанс',
                                          callback_data=cancel_support_callback.new(
                                              user_id=contact_id)
                                          )
                     )
    return keyboard


async def cancel_support(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Закінчити сеанс', callback_data=cancel_support_callback.new(user_id=user_id))]
        ]
    )
