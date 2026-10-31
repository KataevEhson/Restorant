from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from service import *




users_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Покозать меню"),KeyboardButton(text="Покозать мои заказы")],
        [KeyboardButton(text="Заказат блюдо")],
        [KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)




admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить блюдо"), KeyboardButton(text="Изменить блюда")],
        [KeyboardButton(text="Удалить блюда"), KeyboardButton(text="Покозать меню")],
        [KeyboardButton(text="Добавить категорию"), KeyboardButton(text="Изменить категорию")],
        [KeyboardButton(text="Заказат блюдо")],
        [KeyboardButton(text="Мои заказы"), KeyboardButton(text="Помощь")]   
    ],
    resize_keyboard=True
)





async def get_category_button():
    data = await get_category()
    keyboards = []
    for category in data:
        keyboards.append([InlineKeyboardButton(text=f"{category['category_name']}", callback_data=f"category_{category['category_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor





async def get_category_order_button():
    data = await get_category()
    keyboards = []
    for category in data:
        keyboards.append([InlineKeyboardButton(text=f"{category['category_name']}", callback_data=f"category_order_{category['category_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor




async def get_dishes_order_button(cat_id):
    data = await get_dishes_cat_id(cat_id)
    keyboards = []
    for dish in data:
        keyboards.append([InlineKeyboardButton(text=f"{dish['name']}", callback_data=f"dish_order_{dish['dish_id']}")])
    keybor = InlineKeyboardMarkup(inline_keyboard=keyboards)
    return keybor


async def zakas_button(dish_id):
    keybor = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Заказать блюдо", callback_data=f"zakas_{dish_id}")]
    ])
    return keybor
