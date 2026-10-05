import asyncio
from aiogram import Bot, Dispatcher
import handlers
import subscribers

from config import TOKEN


async def main():
    bot = Bot(token = TOKEN)
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    subscribers.init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
