from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


URL = "https://www.krsu.kg/"
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


def fetch_news() -> list:
    response = requests.get(URL, headers = HEADERS, timeout = 10)
    response.raise_for_status()

    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    h2 = soup.find("h2", string = "Новости")

    if h2 is None:
        raise RuntimeError('Не найден заголовок "Новости"!')

    section = h2.find_parent("section")

    if section is None:
        raise RuntimeError("Не найден родитель карточек!")

    cards = section.find_all("div", class_ = PARENT_CLASS)
    news = []

    for card in cards:
        news.append(parse_card(card))

    return news
