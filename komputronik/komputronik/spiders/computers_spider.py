from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from komputronik.items import ComputerItemLoader, GenericItem


class ComputersSpider(CrawlSpider):
    name = "computers"
    start_urls = ["https://www.komputronik.pl/search-filter/5801/komputery-do-gier"]

    rules = (Rule(LinkExtractor(allow=("product")), callback="parse_item"),)

    def parse_item(self, response):
        loader = ComputerItemLoader(item=GenericItem(), response=response)
        loader.add_value(
            "category_url", response.request.headers.get("Referer").decode("utf-8")
        )
        loader.add_value("link", response.url)
        loader.add_xpath("computer_name", "//h1/text()")
        loader.add_xpath("graphic_card", '//tr[th/text()="Karta graficzna"]/td')
        loader.add_xpath("price", '//span[contains(@class, "proper")]/text()')
        yield loader.load_item()
