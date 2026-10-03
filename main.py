from storage import load_news, save_news, find_new_news
from scraper import fetch_news


def main():
    news = fetch_news()
    old_news = load_news()
    new_news = find_new_news(news, old_news)
    print(len(news))
    save_news(old_news, new_news)


if __name__ == "__main__":
    main()
