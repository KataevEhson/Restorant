from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keyboards import *
from aiogram.types import CallbackQuery


router = Router()





@router.message(F.text == "Покозать меню")
@router.message(Command("get_menu"))
async def show_menu(message:Message):
    await message.answer("Выбирите категорию блюда", reply_markup=await get_category_order_button())
    
    
    
@router.callback_query(F.data.startswith('category_order_'))
async def show_menu_dishes(callback: CallbackQuery):
    cat_id = callback.data.split("_")[-1]
    await callback.message.answer("Выберите блюдо:", reply_markup=await get_dishes_order_button(cat_id))
    
    
    
@router.callback_query(F.data.startswith('dish_order_'))
async def show_dish(callback: CallbackQuery):
    dish_id = callback.data.split("_")[-1]
    data = await get_dishes_id(dish_id)
    await callback.message.answer_photo(photo=data['file_id'], caption=f"Name: {data['name']}\nЦена: {data['price']}", reply_markup=await zakas_button(dish_id))
    await callback.answer()
