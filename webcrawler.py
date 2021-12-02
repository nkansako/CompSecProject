import config
from bs4 import BeautifulSoup
import requests


def crawl(searchwords: list):
    print("Webcrawler.py:Argument searchwords given:",searchwords)
    retval = []
    if len(searchwords) != 0:
        for searchword in searchwords:
            print("Webcrawler.py:Searchword:",searchword)
            search = config.search_beginning + searchword + config.search_end
            page = requests.get(search)

            soup = BeautifulSoup(page.content, "html.parser")
            newUrls = []
            for link in soup.find_all("a", "teaser"):
                tmp = link.get("href")
                print("Webcrawler.py:Found link:",tmp,". Appending to newUrls.")

                newUrls.append(config.crawl_base+tmp)

            for url in newUrls:
                page = requests.get(url)
                print("Webcrawler.py:Souping through:",page)
                soup = BeautifulSoup(page.content, "html.parser")

                for hit in soup.find_all(attrs={'class': 'body'}):
                    text = hit.text.strip()
                    if "Postiosoite" in text:
                        print("Webcrawler.py:Found postiosoite, breaking.")
                        break
                    if len(text) != 0:
                        retval.append((url, text))
    return retval
