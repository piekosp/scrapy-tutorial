import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import strip_html5_whitespace, replace_tags


def remove_nbps(value):
    return value.replace("\u00a0", "")


class ComputerItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    computer_name_in = MapCompose(strip_html5_whitespace)
    graphic_card_in = MapCompose(replace_tags, strip_html5_whitespace)
    price_in = MapCompose(strip_html5_whitespace, remove_nbps)


class GenericItem(scrapy.Item):
    category_url = scrapy.Field()
    link = scrapy.Field()
    computer_name = scrapy.Field()
    graphic_card = scrapy.Field()
    price = scrapy.Field()
