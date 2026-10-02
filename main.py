import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


URL = "https://www.krsu.kg/"
FILE_NEWS = "news.json"
PARENT_CLASS = "swiper-slide-wrapper slider-item-news__wrapper"
CLASS_TITLE = "news-card-label-default slider-item-news__title"
CLASS_DATE = "news-card-data slider-item-news__description"

MONTHS = {
    "января": "01", "февраля": "02", "марта": "03",
    "апреля": "04", "мая": "05", "июня": "06",
    "июля": "07", "августа": "08", "сентября": "09",
    "октября": "10", "ноября": "11", "декабря": "12",
}


def normalize_date(text_date: str) -> str:
    text_date = text_date.split()[:3]

    return text_date[0] + "." + MONTHS[text_date[1]] + "." + text_date[2]


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
    with open(FILE_NEWS, "r", encoding="utf-8") as file:
        return json.load(file)


def save_news(news: list):
    with open(FILE_NEWS, "w", encoding = "utf-8") as file:
        json.dump(news, file, ensure_ascii = False, indent = 4)


def find_new_news(news: list, old_news: list) -> list:
    old_links = [a["link"] for a in old_news]
    
    return [a for a in news if a["link"] not in old_links]


def fetch_news() -> list:
    response = requests.get(URL)
    response.raise_for_status()

    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    title_news_parent = soup.find("h2", string = "Новости").find_parent("section", class_ = "container-flex-col g-48")
    cards = title_news_parent.find_all("div", class_ = PARENT_CLASS)
    news = []

    for card in cards:
        news.append(parse_card(card))

    return news


def main():
    news = fetch_news()
    old_news = load_news()
    new_news = find_new_news(news, old_news)
    print(new_news)
    save_news(news)


if __name__ == "__main__":
    main()
