import asyncio
from aiogram import Dispatcher
from aiogram.client.session import aiohttp
from aiogram.fsm.storage.redis import RedisStorage

from DataBase.TablesCreator import tables_god
from DataBase.base import User
from Middleware.trottling import ThrottlingMiddleware
from handlers.admin import admin_menu, orders
from handlers.users import start, menu, register, get_order
from loader import all_data
from xls_export.xls import export_to_xls

data = all_data()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage=storage)


async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")
    user = User()
    # Технические роутеры
    await export_to_xls()

    dp.include_router(start.router)
    dp.include_router(admin_menu.router)
    dp.include_router(menu.router)
    dp.include_router(register.router)
    dp.include_router(get_order.router)
    dp.include_router(orders.router)
    dp.message.middleware(ThrottlingMiddleware())
    session = aiohttp.ClientSession()
    # use the session here

    await session.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    tables_god()
    asyncio.run(main())


