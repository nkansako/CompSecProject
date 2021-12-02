import config
from bs4 import BeautifulSoup
import requests


def crawl(searchwords: list):
    texts = []
    if len(searchwords) != 0:
        for searchword in searchwords:
            search = config.search_beginning + searchword + config.search_end
            page = requests.get(search)

            soup = BeautifulSoup(page.content, "html.parser")
            newUrls = []
            for link in soup.find_all("a", "teaser"):
                tmp = link.get("href")

                newUrls.append(config.crawl_base+tmp)

            for url in newUrls:
                page = requests.get(url)

                soup = BeautifulSoup(page.content, "html.parser")

                for hit in soup.find_all(attrs={'class': 'body'}):
                    text = hit.text.strip()
                    if "Postiosoite" in text:
                        break
                    if len(text) != 0:
                        texts.append(text)
    return texts
