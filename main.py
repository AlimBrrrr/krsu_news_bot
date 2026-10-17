import asyncio
from aiogram import Bot, Dispatcher
import handlers
import subscribers
import service

from config import TOKEN, INTERVAL


async def main():
    bot = Bot(token = TOKEN)
    dp = Dispatcher()
    dp.include_routers(handlers.router)
    subscribers.init_db()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(news_loop(bot))
        await dp.start_polling(bot)


async def news_loop(bot):
    while True:
        try:
            news = await service.check_news()
            if news:
                msg = handlers.format_news(news)
                for user in subscribers.get_subscribers():
                    await bot.send_message(chat_id = user, text = msg, parse_mode = 'HTML')
            print(news)
        except Exception as e:
            print("Произошла ошибка:", e)
        
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
