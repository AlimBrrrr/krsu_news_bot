import asyncio
import html
import logging

from scraper import fetch_news
from storage import load_news, save_news, find_new_news


logger = logging.getLogger(__name__)


async def check_news() -> list[dict]:
    old_news = load_news()
    news = await asyncio.to_thread(fetch_news)

    if not old_news:
        save_news(old_news, news)
        logger.info("Файл с новостями был пуст. Уже обновлен!")

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


def format_news(items: list[dict]) -> str:
    msg = ""
    for item in items:
        title, link, date = item["title"], item["link"], item["date"]
        title = html.escape(title, quote = True)
        link = html.escape(link, quote = True)
        date = html.escape(date, quote = True)
        msg += (f'<b> - {title}</b>\n{date}, <a href="{link}">Ссылка</a>\n\n')

    return msg
