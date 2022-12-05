import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def strip_value(value: str):
    return value.strip()


class ScrapyEplanningItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field(input_processor=MapCompose(strip_value), output_processor=TakeFirst())
    number = scrapy.Field(input_processor=MapCompose(strip_value), output_processor=TakeFirst())
    fax = scrapy.Field(input_processor=MapCompose(strip_value), output_processor=TakeFirst())
    e_mail = scrapy.Field(input_processor=MapCompose(strip_value), output_processor=TakeFirst())
    all_addresses = scrapy.Field()
