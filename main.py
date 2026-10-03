import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


URL = "https://www.krsu.kg/"
FILE_NEWS = "news.json"
PARENT_CLASS = "swiper-slide-wrapper slider-item-news__wrapper"
CLASS_TITLE = "news-card-label-default slider-item-news__title"
CLASS_DATE = "news-card-data slider-item-news__description"
HEADERS = {"User-Agent": "https://github.com/AlimBrrrr/krsu_news_bot (educational project)"}

MONTHS = {
    "января": "01", "февраля": "02", "марта": "03",
    "апреля": "04", "мая": "05", "июня": "06",
    "июля": "07", "августа": "08", "сентября": "09",
    "октября": "10", "ноября": "11", "декабря": "12",
}


def normalize_date(text_date: str) -> str:
    try:
        norm_text_date = text_date.split()[:3]

        return norm_text_date[0] + "." + MONTHS[norm_text_date[1]] + "." + norm_text_date[2]
    except (ValueError, KeyError):
        return text_date


def parse_card(card) -> dict:
    title = card.find("div", class_ = CLASS_TITLE).get_text(strip=True)
    link = urljoin(URL, card.find("a")["href"])
    date_element = card.find("div", class_ = CLASS_DATE)
    date_element = normalize_date(date_element.get_text(strip=True)) if date_element else ""

    return {
        "title": title,
        "link": link,
        "date": date_element,
    }


def load_news() -> list:
    try:
        with open(FILE_NEWS, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return []


def save_news(old_news: list, new_news: list):
    with open(FILE_NEWS, "w", encoding = "utf-8") as file:
        json.dump(old_news + new_news, file, ensure_ascii = False, indent = 4)


def find_new_news(news: list, old_news: list) -> list:
    old_links = [a["link"] for a in old_news]
    
    return [a for a in news if a["link"] not in old_links]


def fetch_news() -> list:
    response = requests.get(URL, headers = HEADERS, timeout = 10)
    response.raise_for_status()

    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    heading = soup.find("h2", string = "Новости").find_parent("section")

    if heading is None:
        raise RuntimeError('Не найден заголовок "Новости"')

    cards = heading.find_all("div", class_ = PARENT_CLASS)
    news = []

    for card in cards:
        news.append(parse_card(card))

    return news


def main():
    news = fetch_news()
    old_news = load_news()
    new_news = find_new_news(news, old_news)
    print(len(news))
    save_news(old_news, new_news)


if __name__ == "__main__":
    main()
