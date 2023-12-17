from aiogram import Bot
from aiogram.types import Message, FSInputFile
import openpyxl
import psycopg2

from config import host, user, password, db_name, port

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port
)


def export_data(file_path):
    connect = connection.cursor()

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    connect.execute("SELECT product_uuid, title, price, category, brand FROM product")

    sheet.append(
        ['Product UUID', 'Title', 'Price', 'Category', 'Brand'])

    for row in connect:
        sheet.append(row)

    workbook.save(file_path)

    connect.close()
    connect.close()


async def get_document(message: Message, bot: Bot):
    export_data('D:/TelegramShopProject/products.xlsx')
    document = FSInputFile(path='D:/TelegramShopProject/products.xlsx')
    await bot.send_document(message.chat.id, document=document)