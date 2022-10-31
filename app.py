import asyncio
from aiogram import Dispatcher
from aiogram.client.session import aiohttp
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from DataBase.TablesCreator import tables_god
from loader import all_data

data = all_data()
bot = data.get_bot()
storage = RedisStorage.from_url(data.redis_url)
dp = Dispatcher(storage)

async def main():
    bot_info = await bot.get_me()
    print(f"Hello, i'm {bot_info.first_name} | {bot_info.username}")

    # Технические роутеры

    #dp.include_router(pg_mg.router)
    #dp.message.middleware(ThrottlingMiddleware())

    session = aiohttp.ClientSession()
    # use the session here

    await session.close()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    tables_god()
    asyncio.run(main())


