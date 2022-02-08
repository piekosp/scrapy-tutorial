from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url
from scrapy import Request

from komputronik.items import ComputerItemLoader, GenericItem


class ComputerSpider(Spider):
    name = "computer_spider"
    link_extractor = LinkExtractor(allow=("product"))

    def start_requests(self):
        urls = [
            "https://www.komputronik.pl/search-filter/5022/laptopy-do-gier",
            "https://www.komputronik.pl/search-filter/5801/komputery-do-gier",
        ]
        for url in urls:
            yield Request(url, callback=self.paginator, meta={"category_url": url})

    def paginator(self, response):
        pages = int(
            response.xpath(
                '//div[contains(@class, "pagination")]/ul/li[last()-1]/a/text()'
            ).get()
        )
        base_url = response.request.url
        for i in range(1, pages + 1):
            if i == 1:
                yield Request(base_url, callback=self.extract_items, dont_filter=True)
            url = base_url + f"?p={i}"
            yield Request(url, callback=self.extract_items)

    def extract_items(self, response):
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_item)

    def parse_item(self, response):
        loader = ComputerItemLoader(item=GenericItem(), response=response)
        loader.add_value("category_url", response.meta["category_url"])
        loader.add_value("link", response.url)
        loader.add_xpath("computer_name", "//h1/text()")
        loader.add_xpath("graphic_card", '//tr[th/text()="Karta graficzna"]/td')
        loader.add_xpath("price", '//span[contains(@class, "proper")]/text()')
        yield loader.load_item()
