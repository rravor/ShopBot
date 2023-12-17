from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from classes.classes import AddUser, UpdateUser
import psycopg2
from config import host, user, password, db_name, port

router = Router()


connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port=port
)


@router.message(F.text.lower() == 'зарегистрироваться')
async def registration_user(message: Message, state: FSMContext):
    with connection.cursor() as connect:
        connect.execute(f"SELECT username FROM shop_user")
        usernames = ', '.join([str(item) for item in connect.fetchall()])
        if message.from_user.username in usernames:
            await message.answer('Вы уже зарегистрированы!')
        else:
            await state.set_state(AddUser.enter_name)
            await message.answer('Введи имя!')


@router.message(AddUser.enter_name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(enter_name=message.text)
    await state.set_state(AddUser.enter_phone_number)
    await message.answer("Введи номер телефона!")


@router.message(AddUser.enter_phone_number)
async def form_phone(message: Message, state: FSMContext):
    await state.update_data(enter_phone_number=message.text)
    await state.set_state(AddUser.enter_email)
    await message.answer("Введи почту!")


@router.message(AddUser.enter_email)
async def form_phone(message: Message, state: FSMContext):
    await state.update_data(enter_email=message.text)
    await state.set_state(AddUser.enter_address)
    await message.answer("Введи адрес!")


@router.message(AddUser.enter_address)
async def form_phone(message: Message, state: FSMContext):
    with connection.cursor() as connect:
        data = await state.update_data(enter_address=message.text)

        enter_name = data['enter_name']
        enter_username = message.from_user.username
        enter_phone_number = data['enter_phone_number']
        enter_email = data['enter_email']
        enter_address = data['enter_address']

        connect.execute(f"INSERT INTO shop_user (name, username, phone_number, email, address) VALUES ('{enter_name}', '{enter_username}', '{enter_phone_number}', '{enter_email}', '{enter_address}')")
        connection.commit()

        await state.clear()
        await message.answer('User успешно зарегистрирован')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@router.message(F.text.lower() == 'личный кабинет')
async def get_all_products(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.set_state(UpdateUser.id)
        cursor.execute(f"SELECT * FROM shop_user WHERE username = '{message.from_user.username}';")
        user = ', '.join([str(item) for item in cursor.fetchall()])
        await message.answer(f"Пользователь - {user}")


@router.message(F.text.lower() == 'обновить пользователя')
async def update_product_request(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(id=message.text)
        await state.set_state(UpdateUser.data)
        cursor.execute(f"SELECT * FROM shop_user WHERE username = '{message.from_user.username}'")
        choice = ', '.join([str(item) for item in cursor.fetchone()])
        await message.answer(f"Пользователь - {choice}\nВведи новые данные пользователя в виде:\nname, phone_number, email, address")


@router.message(UpdateUser.data)
async def update_product(message: Message, state: FSMContext):
    with connection.cursor() as cursor:
        await state.update_data(data={"data": message.text})
        data = message.text.split(', ')
        cursor.execute(f"UPDATE shop_user SET (name, phone_number, email, address) = ('{data[0]}', '{data[1]}', '{data[2]}','{data[3]}') WHERE username = '{message.from_user.username}'")
        connection.commit()
        await message.answer("Пользователь успешно обновлён")
        await state.clear()