import asyncio
import html
import logging
from datetime import date

from scraper import fetch_news
from storage import load_news, save_news, find_new_news


logger = logging.getLogger(__name__)


async def check_news() -> list[dict]:
    old_news = load_news()
    news = await asyncio.to_thread(fetch_news)

    if not old_news:
        save_news(old_news, news)
        logger.info("The news.json was empty. It has updated already!")

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
    i = 0
    for item in items:
        i += 1
        title, link, daten = item["title"], item["link"], item["date"]
        title = html.escape(title, quote = True)
        link = html.escape(link, quote = True)
        daten = date.fromisoformat(html.escape(daten, quote = True))
        daten = daten.strftime("%d.%m.%Y")
        msg += (f'<b>{i}. </b><a href="{link}">{title}</a>\n📅 {daten}\n\n')

    return msg
