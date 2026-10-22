import asyncio
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramForbiddenError
from handlers import router
import subscribers
import service

from config import TOKEN, INTERVAL


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), RotatingFileHandler("bot.log", maxBytes = 2**13, encoding="utf-8")]
    )

    bot = Bot(token = TOKEN)
    dp = Dispatcher()
    dp.include_routers(router)
    subscribers.init_db()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(news_loop(bot))
        await dp.start_polling(bot)


async def news_loop(bot):
    while True:
        try:
            news = await service.check_news()
            logger.info("News detected: %s", len(news))

            if news:
                msg = service.format_news(news)
                for user in subscribers.get_subscribers():
                    try:
                        await bot.send_message(chat_id = user, text = msg, parse_mode = 'HTML')
                        await asyncio.sleep(0.05)
                    except TelegramForbiddenError:
                        logger.warning("The user %s blocked the bot", user)

                        if subscribers.remove_subscriber(user):
                            logger.info("The user %s was removed from db successfully", user)
                    except Exception:
                        logger.exception("An error has occured: %s", user)

        except Exception:
            logger.exception("An error has occured")
        
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot was stopped manually")
