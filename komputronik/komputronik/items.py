# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import strip_html5_whitespace, replace_entities, replace_tags


def remove_nbps(value):
    return value.replace("\u00a0", "")


class KomputronikItem(scrapy.Item):
    category_url = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    computer_name = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace), output_processor=TakeFirst()
    )
    graphic_card = scrapy.Field(
        input_processor=MapCompose(replace_tags, strip_html5_whitespace),
        output_processor=TakeFirst(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(strip_html5_whitespace, remove_nbps),
        output_processor=TakeFirst(),
    )
