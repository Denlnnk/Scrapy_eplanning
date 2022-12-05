# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyEplanningItem(scrapy.Item):
    name = scrapy.Field()
    number = scrapy.Field()
    fax = scrapy.Field()
    e_mail = scrapy.Field()
    all_addresses = scrapy.Field()
