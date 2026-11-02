import asyncio
import logging
from logging.handlers import RotatingFileHandler
from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
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
                await sending_news(bot, news)

        except Exception as e:
            logger.exception("An error has occured: %s", e)
        
        await asyncio.sleep(INTERVAL)


async def sending_news(bot, news):
    users = subscribers.get_subscribers()
    dead_users = set()
    news = service.format_news(news).split("\n\n")
    news = [x for x in news if x.strip() != ""]
    for new in news:
        for user in users:
            if user in dead_users:
                continue

            for attempt in range(5):
                try:
                    await bot.send_message(chat_id = user, text = new, parse_mode = "HTML")
                    logger.info("User %s received the news: %s", user, new[20:60] + "...")
                    await asyncio.sleep(0.05)
                    break
                except TelegramForbiddenError:
                    logger.warning("The user %s blocked the bot", user)
                    subscribers.remove_subscriber(user)
                    dead_users.add(user)
                    break
                except TelegramRetryAfter as e:
                    logger.warning("The limit of requests has reached")
                    await asyncio.sleep(e.retry_after)
                except Exception as e:
                    logger.warning("An error has occured: %s", e)
                    break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot was stopped manually")
