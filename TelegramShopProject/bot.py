import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
import commands
from registration import registration
from crud import crud


async def main() -> None:
    TOKEN = '6650988748:AAHGxvuWSF47T1Gec7F90eUwXFbOd8f9-QI'
    dp = Dispatcher()
    dp.include_routers(crud.router, registration.router, commands.router)
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
