from aiogram.utils.callback_data import CallbackData

place_callback = CallbackData("offer", "number", "choice", "restaurant")
rs_callback = CallbackData("rs", "number")
support_callback = CallbackData(
    "ask_support", "messages", "user_id", "as_user"
)
cancel_support_callback = CallbackData("cancel_support", "user_id")
menu_callback = CallbackData(
    "show_menu", "level", "category", "subcategory", "item_id"
)
buy_item_callback = CallbackData("buy", "item_id")
admin_place_callback = CallbackData(
    "admin_place", "method", "place_id", "value"
)
cart_callback = CallbackData("cart", "action", "item_id")
order_callback = CallbackData("order", "action", "id", "value")
