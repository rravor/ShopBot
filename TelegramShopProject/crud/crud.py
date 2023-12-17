from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import psycopg2
from config import host, user, password, db_name, port
from classes.classes import AddProduct, DeleteProduct, UpdateProduct, CheckProduct, CheckProductCategory, CheckProudctBrend, GetExcelFile
from excel.uploadxlsx import get_document
from excel.loadxlsx import load_from_excel
import os

router = Router()


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'добавить продукт')
async def add_product(message: Message, state: FSMContext):
    await state.set_state(AddProduct.data)
    await message.answer(f'Введи данные продукта в виде:\ntitle, price, category_id, brand_id')


@router.message(AddProduct.data)
async def add_product_by_datas(message: Message, state: FSMContext):
    with connection.cursor() as connect:
        await state.update_data(data={"data": message.text})
        data = message.text.split(', ')
        connect.execute(f"SELECT product_insert('{data[0]}', {int(data[1])}, {int(data[2])}, {int(data[3])})")
        connection.commit()
        await message.answer("Продукт усещно добавлен")
        await state.clear()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'удалить продукт')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(DeleteProduct.id)
    await message.answer("Введи uuid продукта")


@router.message(DeleteProduct.id)
async def delete_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT Delete_product('{message.text}')")
        connection.commit()
        await message.answer("Продукт успешно удалён")
        await state.clear()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

product_to_update = None


@router.message(F.text.lower() == 'обновить продукт')
async def update_product(message: Message, state: FSMContext):
    await state.set_state(UpdateProduct.id)
    await message.answer("Введи uuid продукта")


@router.message(UpdateProduct.id)
async def update_product_request(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        global product_to_update
        product_to_update = message.text
        await state.update_data(id=message.text)
        await state.set_state(UpdateProduct.data)
        cursor.execute(f"SELECT * FROM product WHERE product_uuid = '{message.text}'")
        choice = ', '.join([str(item) for item in cursor.fetchone()])
        await message.answer(f"Продукт - {choice}\nВведи новые данные продукта в виде:\ntitle, price, category_id, brand_id")


@router.message(UpdateProduct.data)
async def update_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(data={"data": message.text})
        data = message.text.split(', ')
        cursor.execute(f"SELECT UpdateProduct('{data[0]}', {int(data[1])}, {int(data[2])}, {int(data[3])}, '{product_to_update}');")
        connection.commit()
        await message.answer("Продукт успешно обновлён")
        await state.clear()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'посмотреть продукты по бренду')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(CheckProudctBrend.id)
    await message.answer("Введи id бренда")


@router.message(CheckProudctBrend.id)
async def get_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT * FROM SelectProductsByBrand('{message.text}');")
        products = ', \n'.join([f"{str(item)}\n" for item in cursor.fetchone()])
        await message.answer(f"Продукты - {products}")
        await state.clear()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'посмотреть продукты по категории')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(CheckProductCategory.id)
    await message.answer("Введи id категории")


@router.message(CheckProductCategory.id)
async def get_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT * FROM SelectProductsByCategory('{message.text}');")
        products = ', \n'.join([f"{str(item)}\n" for item in cursor.fetchone()])
        await message.answer(f"Продукты - {products}")
        await state.clear()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'посмотреть продукт')
async def check_detail_product(message: Message, state: FSMContext):
    await state.set_state(CheckProduct.id)
    await message.answer("Введи uuid продукта")


@router.message(CheckProduct.id)
async def get_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        cursor.execute(f"SELECT * FROM SelectProductInfo('{message.text}');")
        product = ', '.join([f"{str(item)}\n" for item in cursor.fetchone()])
        await message.answer(f"Продукт - {product}")
        await state.clear()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'посмотреть все продукты')
async def get_all_products(message: Message):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM SelectAllProducts();')
        products = ', \n'.join([f"{str(item)}\n" for item in cursor.fetchall()])
        await message.answer(f"Продукты - {products}")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'посмотреть 10 из последних продуктов')
async def get_ten_last_added_produtcs(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM GetTenProducts();')
        products = ', \n'.join([f"{str(item)}\n" for item in cursor.fetchall()])
        await message.answer(f"Продукты - {products}")
        await state.clear()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@router.message(F.text.lower() == 'выгрузка в excel')
async def upload_xslx(message: Message, bot: Bot, state: FSMContext):
    await get_document(message, bot)
    await message.answer("Успешо выгрузил")
    await state.clear()


@router.message(F.text.lower() == 'загрузка с excel')
async def get_xlsx_file(message: Message, state: FSMContext):
    await message.answer('Отправьте файл xlsx формата.')
    await state.set_state(GetExcelFile.file)


@router.message(GetExcelFile.file)
async def load_xlsx_file(message: Message, bot: Bot, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, r"D:/TelegramShopProject/files/file.xlsx")
    load_from_excel('D:/TelegramShopProject/files/file.xlsx')
    os.remove('D:/TelegramShopProject/files/file.xlsx')
    await state.clear()
    await message.answer('Успешно выгружен')