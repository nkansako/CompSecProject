import config
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests


def crawl(searchwords: list):
    if len(searchwords) != 0:
        for searchword in searchwords:
            search = config.search_beginning + searchword + config.search_end
            page = requests.get(search)

            soup = BeautifulSoup(page.content, "html.parser")
            newUrls = []
            for link in soup.find_all("a", "teaser"):
                print(link.get("href"))

                newUrls.append(config.crawl_base+link.get("href"))

            for url in newUrls:
                page = requests.get(url)

                soup = BeautifulSoup(page.content, "html.parser")

                for hit in soup.find_all(attrs={'class': 'body'}):
                    text = hit.text.strip()
                    print(text)


crawl(["mfa"])