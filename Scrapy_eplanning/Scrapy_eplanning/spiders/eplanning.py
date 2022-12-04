import scrapy
from scrapy import FormRequest


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response, **kwargs):
        counties_url = response.xpath('//td/a/@href').get()
        # for url in counties_url:
        #     if url == '#':
        #         pass
        #     else:
        yield scrapy.Request(counties_url, callback=self.parse_country)

    def parse_country(self, response):
        received_app_url = response.xpath(
            '//span[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').get()
        absolute_received_app_url = response.urljoin(received_app_url)
        yield scrapy.Request(absolute_received_app_url, callback=self.parse_form)

    def parse_form(self, response):
        pass
