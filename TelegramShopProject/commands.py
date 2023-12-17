from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import types
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    buttons = [
        [types.KeyboardButton(text="зарегистрироваться")],
        [types.KeyboardButton(text="добавить продукт")],
        [types.KeyboardButton(text="удалить продукт")],
        [types.KeyboardButton(text="обновить продукт")],
        [types.KeyboardButton(text="посмотреть продукт")],
        [types.KeyboardButton(text="посмотреть все продукты")],
        [types.KeyboardButton(text="посмотреть 10 из последних продуктов")],
        [types.KeyboardButton(text="посмотреть продукты по категории")],
        [types.KeyboardButton(text="посмотреть продукты по бренду")],
        [types.KeyboardButton(text='выгрузка в excel')],
        [types.KeyboardButton(text='загрузка с excel')]
    ]
    b = types.ReplyKeyboardMarkup(keyboard=buttons)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!", reply_markup=b)