from aiogram.utils.callback_data import CallbackData

place_callback = CallbackData('offer', 'number', 'choice')
rs_callback = CallbackData('rs', 'number')
support_callback = CallbackData('ask_support', 'messages', 'user_id', 'as_user')
cancel_support_callback = CallbackData('cancel_support', 'user_id')
