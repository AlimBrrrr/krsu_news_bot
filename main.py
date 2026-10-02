import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

url = "https://www.krsu.kg/"
response = requests.get(url)
response.raise_for_status()

content = response.text
soup = BeautifulSoup(content, "html.parser")
cards = soup.find_all("div", class_ = "swiper-slide-wrapper slider-item-news__wrapper")
news = []
months = {
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
    return text_date[0] + "." + months[text_date[1]] + "." + text_date[2]


def parse_card(card):
    title = card.find("div", class_ = "news-card-label-default slider-item-news__title").get_text(strip=True)
    link = urljoin(url, card.find("a")["href"])
    dictionary = {"title": title, "link": link}
    date_element = card.find("div", class_ = "news-card-data slider-item-news__description")

    if date_element:
        dictionary["date"] = normalize_date(date_element.get_text(strip=True))

    return dictionary


for card in cards:
    news.append(parse_card(card))

with open("news.json", "w", encoding="utf-8") as file:
    json.dump(news, file, ensure_ascii=False, indent=4)

with open("news.json", "r", encoding="utf-8") as file:
    print(json.load(file))

# titles = [x["title"] for x in news]
# print(*set([x for x in titles if titles.count(x) > 1]), sep="\n")

# print(*news, sep="\n\n")
