import requests
from bs4 import BeautifulSoup


def scrape_bbc_headlines():
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headlines = []
    headline_elements = soup.find_all("h3", class_="gs-c-promo-heading__title")

    for element in headline_elements:
        headline = element.text.strip()
        headlines.append(headline)

    return headlines


def main():
    print("BBC News Headlines Scraper")
    headlines = scrape_bbc_headlines()

    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline}")


if __name__ == "__main__":
    main()
