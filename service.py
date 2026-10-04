import asyncio

from scraper import fetch_news
from storage import load_news, save_news, find_new_news


async def get_news() -> list:
    old_news = load_news()
    news = await asyncio.to_thread(fetch_news)

    if len(old_news) == 0:
        save_news(old_news, news)

        return []

    new_news = find_new_news(news, old_news)
    save_news(old_news, new_news)

    return new_news
