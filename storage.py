import json
import logging


FILE_NEWS = "news.json"
logger = logging.getLogger(__name__)


def load_news() -> list:
    try:
        with open(FILE_NEWS, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError) as e:
        logger.exception("Ошибка чтения файла: %s", e)
        return []


def save_news(old_news: list, new_news: list):
    with open(FILE_NEWS, "w", encoding = "utf-8") as file:
        json.dump(old_news + new_news, file, ensure_ascii = False, indent = 4)


def find_new_news(news: list, old_news: list) -> list:
    old_links = set([a["link"] for a in old_news])
    
    return [a for a in news if a["link"] not in old_links]
