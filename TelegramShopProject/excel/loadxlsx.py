import openpyxl
import psycopg2
from aiogram import Bot
from aiogram.types import Message, document
from psycopg2 import sql

from config import host, user, password, db_name, port

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port
)


def load_from_excel(file_path):
    connect = connection.cursor()

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    for row in sheet.iter_rows(min_row=2):
        product_uuid, title, price, category, brand = [cell.value for cell in row][:6]
        product_uuid = str(product_uuid)
        title = str(title)
        price = int(price)
        category = int(category)
        brand = int(brand)

        connect.execute(
            sql.SQL(f"INSERT INTO product (product_uuid, title, price, category, brand) VALUES ('{product_uuid}', '{title}', {price}, {category}, {brand})")
        )

    connect.close()
    connection.commit()
    connect.close()
    workbook.close()