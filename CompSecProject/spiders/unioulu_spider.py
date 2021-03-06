import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup


# item class
class OuluItem(scrapy.Item):
    link = scrapy.Field()


class UniouluSpider(scrapy.Spider):
    name = "unioulu"
    allowed_domains = ["oulu.fi"]
    start_urls = [
    "https://www.oulu.fi/fi/search?search_api_fulltext=mittaustekniikka&field_targeting=All"
    ]

    BASE_URL = 'https://www.oulu.fi'

    def parse(self, response):
        soup = BeautifulSoup(response.body, features="html.parser")

        hyperlinks = []
        for link in soup.find_all("a", "teaser"):
            tmp = self.BASE_URL + link.get("href")
            hyperlinks.append(tmp)
            print(tmp)


        #https://www.oulu.fi/fi/uutiset/opiskelija-ota-mfa-kayttoosi-lokakuun-aikana
        #for hit in soup.find_all(attrs={​​​​​​​​​'class' : 'body field--type-text-with-summary field--view-mode-full text-long'}​​​​​​​​​):
        #    text = hit.text.strip()
        #    print(text)

    def parse_attr(self, response):
        item = OuluItem()
        item["link"] = response.url
        print(item)
        return item