from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *
from keyboards import *
from aiogram.types import CallbackQuery


router = Router()


class AddDishes(StatesGroup):
    get_catgory_id= State()
    get_name = State()
    get_caption = State()
    get_price = State()
    get_photo_id = State()
    
    
class AddCategory(StatesGroup):
    get_title = State()
    
    
class Change_category(StatesGroup):
    get_cat_id = State()
    get_new_name = State()
    


class Changedishes(StatesGroup):
    get_dihse_id = State()
    get_catgory_id= State()
    get_name = State()
    get_caption = State()
    get_price = State()
    get_photo_id = State()
    


class Delete_dish(StatesGroup):
    get_dish_id = State()

    



@router.message(F.text == "Добавить категорию")
@router.message(Command("add_category"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        await message.answer("Введите имя категории:")
        await state.set_state(AddCategory.get_title)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()


@router.message(AddCategory.get_title)
async def add_category_title(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    data = await state.get_data()
    status = await create_category_db(data['title'])
    if status:
        await message.answer("Ваша категория создана")
        
    else:
        await message.answer("Ошибка при создании категория!")
    await state.clear()





@router.message(F.text == "Добавить блюдо")
@router.message(Command("add_dishes"))
async def add_category(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        button = await get_category_button()
        await message.answer("Выбирите категорию", reply_markup= button)
        await state.set_state(AddDishes.get_catgory_id)
    else:
        await message.answer("Только админ может создавать книги!")
        await state.clear()



@router.callback_query(AddDishes.get_catgory_id, F.data.startswith("category_"))
async def get_catgory_id_dishes(callback : CallbackQuery, state : FSMContext):
    cat_id = callback.data.split("_")[1]
    await state.update_data(category_id = cat_id)
    await callback.answer("Категория выбрана")
    await callback.message.answer("Введите имя блюдо: ")
    await state.set_state(AddDishes.get_name)




@router.message(AddDishes.get_name)
async def get_name_dishes(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите описание блюдо: ")
    await state.set_state(AddDishes.get_caption)
    
@router.message(AddDishes.get_caption)
async def get_caption_dishes(message: Message, state: FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Введите ценю блюдо: ")
    await state.set_state(AddDishes.get_price)
    
    
@router.message(AddDishes.get_price)
async def get_price_dishes(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer("Отправте фото: ")
    await state.set_state(AddDishes.get_photo_id)
    
@router.message(AddDishes.get_photo_id)
async def get_photo_id_dishes(message: Message, state: FSMContext):
    if not message.photo:
            await message.answer("Вы отправили не фото пожайлусто отправте фото блюда")
            return None
    photo = message.photo[-1]
    
    await state.update_data(file_id = photo.file_id)
    data = await state.get_data()
    if await create_dishes_db(data['category_id'], data['name'], data['caption'], data['price'], data['file_id']):
        await message.answer("Блюдо добавлено удачно")
    else:
        await message.answer("При добовлении блюда произошла ошибка")
    await state.clear()

    






@router.message(Command("change_category"))
async def change_categoy_router(message : Message , state : FSMContext):
    button = await get_category_button()
    await message.answer("Выберите категорию каторую хотите изменитъ: ", reply_markup=button)
    await state.set_state(Change_category.get_cat_id)





@router.callback_query(Change_category.get_cat_id, F.data.startswith("category_"))
async def get_catgory_id_dishes(callback : CallbackQuery, state : FSMContext):
    cat_id = callback.data.split("_")[1]
    await state.update_data(category_id = cat_id)
    await callback.answer("Категория выбрана")
    await callback.message.answer("Введите новое имя категории: ")
    await state.set_state(Change_category.get_new_name)





@router.message(Change_category.get_new_name)
async def get_new_category_name(message : Message , state : FSMContext):
    await state.update_data(new_name = message.text)
    data = await state.get_data()
    await change_category_service(data['category_id'], data['new_name'])
    await message.answer("Ваша категория было успешно изменена!!!")
    await state.clear()


















@router.message(F.text == "Изменить блюда")
@router.message(Command("change_dishes"))
async def change_category_for_me(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        button = await get_dishes_order_button()
        await message.answer("Выберите блюдо:", reply_markup=button)
        await state.set_state(Changedishes.get_dihse_id)
    else:
        await message.answer("Только админ может Изменят блюдо!")
        await state.clear()


@router.callback_query(Changedishes.get_dihse_id, F.data.startswith("dish_order_"))
async def get_chage_(callback : CallbackQuery, state : FSMContext):
    dish_id = int(callback.data.split("_")[-1])
    await state.update_data(dish_id = dish_id)
    await callback.answer("Блюдо выбрано")
    button = await get_category_button()
    await callback.message.answer("Выбери новую категорию: ", reply_markup=button)
    await state.set_state(Changedishes.get_catgory_id)




@router.callback_query(Changedishes.get_catgory_id, F.data.startswith("category_"))
async def get_catgory_id_dishes(callback : CallbackQuery, state : FSMContext):
    cat_id = callback.data.split("_")[1]
    await state.update_data(category_id = cat_id)
    await callback.answer("Категория выбрана")
    await callback.message.answer("Введите новое имя блюда: ")
    await state.set_state(Changedishes.get_name)

@router.message(Changedishes.get_name)
async def change_caption_dishes(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Введите новое описание блюдо: ")
    await state.set_state(Changedishes.get_caption)
    
    
@router.message(Changedishes.get_caption)
async def change_caption_new(message: Message, state: FSMContext):
    await state.update_data(caption = message.text)
    await message.answer("Отправте новый ценник: ")
    await state.set_state(Changedishes.get_price)



@router.message(Changedishes.get_price)
async def change_price(message : Message , state : FSMContext):
    await state.update_data(price = int(message.text))
    await message.answer("Отправте новое фото")
    await state.set_state(Changedishes.get_photo_id)


@router.message(Changedishes.get_photo_id)
async def change_photo_id_dishes(message: Message, state: FSMContext):
    if not message.photo:
            await message.answer("Вы отправили не фото пожайлусто отправте фото блюда")
            return None
    photo = message.photo[-1]
    
    await state.update_data(photo_id = photo.file_id)
    data = await state.get_data()
    if await change_dishe_service(data['dish_id'], data['category_id'], data['name'], data['caption'], data['price'], data['photo_id']):
        await message.answer("Блюдо изменено удачно")
    else:
        await message.answer("При изменени блюда произошла ошибка")
    await state.clear()










@router.message(F.text == "Удалить блюда")
@router.message(Command("change_dishes"))
async def check_delete(message: Message, state: FSMContext):
    if await check_admin(message.from_user.id):
        button = await get_dishes_order_button()
        await message.answer("Выберите блюдо для удаление:", reply_markup=button)
        await state.set_state(Delete_dish.get_dish_id)
    else:
        await message.answer("Только админ может удалят блюдо!")
        await state.clear()


@router.callback_query(Delete_dish.get_dish_id, F.data.startswith("dish_order_"))
async def get_chage_(callback : CallbackQuery, state : FSMContext):
    dish_id = int(callback.data.split("_")[-1])
    await state.update_data(dish_id = dish_id)
    await callback.answer("Блюдо выбрано")
    data = await state.get_data()
    await delete_dish_service(data['dish_id'])
    await callback.message.answer("Ваше блдюдо удалено успешно")
    await state.clear()


class Zakas(StatesGroup):
    get_count = State()


@router.message(F.text == "Заказат блюдо")
@router.message(Command("zakas"))
async def nachat_zakas(message: Message, state: FSMContext):
    button = await get_dishes_order_button()
    await message.answer("Выберите блюдо:", reply_markup= button)


@router.callback_query(F.data.startswith("zakas_"))
async def zakas_bludo(callback: CallbackQuery, state: FSMContext):
    dish_id = callback.data.split("_")[-1]
    await state.update_data(dish_id = int(dish_id))
    await callback.answer("Вы выбрали блюдо")
    await callback.message.answer("Введите количество:")
    await state.set_state(Zakas.get_count)


@router.message(Zakas.get_count)
async def get_kolichestvo(message: Message, state: FSMContext):
    data = await state.get_data()
    await zakas_db(data['dish_id'], message.from_user.id, int(message.text))
    await message.answer("Блюдо заказано!")
    await state.clear()
