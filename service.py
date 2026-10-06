import asyncio

from scraper import fetch_news
from storage import load_news, save_news, find_new_news


async def check_news() -> list[dict]:
    old_news = load_news()
    news = await asyncio.to_thread(fetch_news)

    if not old_news:
        save_news(old_news, news)

        return []

    new_news = find_new_news(news, old_news)

    if new_news:
        save_news(old_news, new_news)

        return new_news

    return []


def get_latest(n) -> list[dict]:
    news = load_news()
    if news:
        news = sorted(news, key = lambda news: news["date"], reverse = True)
        return news[:n]

    return []
