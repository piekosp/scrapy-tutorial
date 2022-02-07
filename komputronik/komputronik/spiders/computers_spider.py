from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.utils.response import get_base_url
from scrapy import Request

from komputronik.items import ComputerItemLoader, GenericItem


class ComputersSpider(CrawlSpider):
    name = "computers"
    start_urls = [
        "https://www.komputronik.pl/search-filter/5801/komputery-do-gier",
        "https://www.komputronik.pl/search-filter/5022/laptopy-do-gier",
    ]
    rules = (
        Rule(
            LinkExtractor(allow=("product")),
            callback="parse_item",
            process_request="process_request",
        ),
    )

    def process_request(self, request, response):
        request.meta["category_url"] = get_base_url(response)
        return request

    def parse_item(self, response):
        loader = ComputerItemLoader(item=GenericItem(), response=response)
        loader.add_value("category_url", response.meta.get("category_url"))
        loader.add_value("link", response.url)
        loader.add_xpath("computer_name", "//h1/text()")
        loader.add_xpath("graphic_card", '//tr[th/text()="Karta graficzna"]/td')
        loader.add_xpath("price", '//span[contains(@class, "proper")]/text()')
        yield loader.load_item()


class TestSpider(Spider):
    name = "c_spider"
    link_extractor = LinkExtractor(allow=("product"))

    def start_requests(self):
        urls = [
            "https://www.komputronik.pl/search-filter/5022/laptopy-do-gier",
            "https://www.komputronik.pl/search-filter/5801/komputery-do-gier",
        ]
        for url in urls:
            yield Request(url, callback=self.paginator)
            yield Request(url, callback=self.extract_items)

    def paginator(self, response):
        pages = int(
            response.xpath(
                '//div[contains(@class, "pagination")]/ul/li[last()-1]/a/text()'
            ).get()
        )
        print(pages)
        for i in range(2, pages + 1):
            url = response.request.url + f"?p={i}"
            print(url)
            yield Request(
                url, callback=self.extract_items, meta=dict(category_url=response.url)
            )

    def extract_items(self, response):
        for link in self.link_extractor.extract_links(response):
            yield Request(link.url, callback=self.parse_item)

    def parse_item(self, response):
        loader = ComputerItemLoader(item=GenericItem(), response=response)
        loader.add_value("category_url", response.meta.get("category_url"))
        loader.add_value("link", response.url)
        loader.add_xpath("computer_name", "//h1/text()")
        loader.add_xpath("graphic_card", '//tr[th/text()="Karta graficzna"]/td')
        loader.add_xpath("price", '//span[contains(@class, "proper")]/text()')
        yield loader.load_item()
