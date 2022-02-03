import scrapy
import csv

from scrapy.loader import ItemLoader
from komputronik.items import KomputronikItem


class ComputersSpider(scrapy.Spider):
    name = "computers"

    def start_requests(self):
        urls = [
            "https://www.komputronik.pl/product/732807/komputronik-infinity-x500-ax4-.html",
            "https://www.komputronik.pl/product/726452/komputronik-infinity-x510-a1-.html",
            "https://www.komputronik.pl/product/742511/komputronik-infinity-x510-m2-.html",
            "https://www.komputronik.pl/product/726453/komputronik-infinity-x510-a2-.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        loader = ItemLoader(item=KomputronikItem(), response=response)
        loader.add_css("computer_name", "h1::text")
        graphic_card_xpath = '//tr[th/text()="Karta graficzna"]/td/text()'
        loader.add_xpath("graphic_card", graphic_card_xpath)
        price_xpath = '//span[contains(@class, "proper")]/text()'
        loader.add_xpath("price", price_xpath)
        yield loader.load_item()
