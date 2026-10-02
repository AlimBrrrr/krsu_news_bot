# KRSU news bot

Бот в телеграме, который уведомляет о новостях в КРСУ (krsu.kg)

## Что умеет
- Парсит раздел "Новости" на главной странице
- Сравнивает новые новости со старыми и обновляет их в файле JSON

## Планируется
- Отправление новостей через бота в Telegram
- Подписка и фильтр по ключевым словам

## Стек
Python, requests, BeautifulSoup. Позже aiogram, SQLite

## Установка и запуск проекта у себя
```bash
git clone https://github.com/ТВОЙ_НИК/krsu_news_bot.git
cd krsu_news_bot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Как работает код
1. `fetch_news()` скачивает страницу сайта КРСУ и вытаскивает карточки новостей
2. `find_new_news` сравнивает их со списком старых новостей в `news.json`
3. Новые новости выводятся на экран, добавляются в файл `news.json` и сохраняются

## Планы
- Telegram бот на aiogram
- Хранение данных в SQLite
- Деплой на сервер