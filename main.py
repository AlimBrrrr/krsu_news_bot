import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json


URL = "https://www.krsu.kg/"
RESPONSE = requests.get(URL)
RESPONSE.raise_for_status()

CONTENT = RESPONSE.text
soup = BeautifulSoup(CONTENT, "html.parser")
title_news_parent = soup.find("h2", string = "Новости").parent.parent.parent.parent.parent
cards = title_news_parent.find_all("div", class_ = "swiper-slide-wrapper slider-item-news__wrapper")
news = []
MONTHS = {
    "января": "01",
    "февраля": "02",
    "марта": "03",
    "апреля": "04",
    "мая": "05",
    "июня": "06",
    "июля": "07",
    "августа": "08",
    "сентября": "09",
    "октября": "10",
    "ноября": "11",
    "декабря": "12",
}


def normalize_date(text_date: str) -> str:
    text_date = text_date.split()[:3]
    return text_date[0] + "." + MONTHS[text_date[1]] + "." + text_date[2]


def parse_card(card) -> dict:
    title = card.find("div", class_ = "news-card-label-default slider-item-news__title").get_text(strip=True)
    link = urljoin(URL, card.find("a")["href"])
    dictionary = {"title": title, "link": link}
    date_element = card.find("div", class_ = "news-card-data slider-item-news__description")

    if date_element:
        dictionary["date"] = normalize_date(date_element.get_text(strip=True))

    return dictionary


def get_news():
    with open("news.json", "r", encoding="utf-8") as file:
        return json.load(file)


def dump_news(news):
    with open("news.json", "w", encoding = "utf-8") as file:
        json.dump(news, file, ensure_ascii = False, indent = 4)


for card in cards:
    news.append(parse_card(card))
