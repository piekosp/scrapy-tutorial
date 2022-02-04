from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor
from komputronik.items import KomputronikItem


class ComputersSpider(CrawlSpider):
    name = "computers"
    start_urls = ["https://www.komputronik.pl/search-filter/5801/komputery-do-gier"]

    rules = (Rule(LinkExtractor(allow=("product")), callback="parse_item"),)

    def parse_item(self, response):
        loader = ItemLoader(item=KomputronikItem(), response=response)
        loader.add_value("category_url", response.request.headers.get("Referer"))
        loader.add_value("link", response.url)
        loader.add_css("computer_name", "h1::text")
        graphic_card_xpath = '//tr[th/text()="Karta graficzna"]/td'
        loader.add_xpath("graphic_card", graphic_card_xpath)
        price_xpath = '//span[contains(@class, "proper")]/text()'
        loader.add_xpath("price", price_xpath)
        yield loader.load_item()
