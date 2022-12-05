import scrapy
from scrapy import FormRequest
from ..items import ScrapyEplanningItem


def parse_table_info(response, value: str):
    if value == 'e-mail':
        return response.xpath(f'//th[text()="{value} :"]/following-sibling::td/a/text()').get()
    return response.xpath(f'//th[text()="{value} :"]/following-sibling::td/text()').get()


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response, **kwargs):
        counties_url = response.xpath('//td/a/@href').get()
        for url in counties_url:
            if url == '#':
                pass
            else:
                yield scrapy.Request(counties_url, callback=self.parse_country)

    def parse_country(self, response):
        received_app_url = response.xpath(
            '//span[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').get()
        absolute_received_app_url = response.urljoin(received_app_url)
        yield scrapy.Request(absolute_received_app_url, callback=self.parse_form)

    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={
                                            'RdoTimeLimit': '42'
                                        },
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages
                                        )

    def parse_pages(self, response):
        file_number_links = response.xpath('//tr/td/a/@href').getall()
        for link in file_number_links:
            absolute_link = response.urljoin(link)
            yield scrapy.Request(absolute_link, callback=self.parse_details)

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse_pages)

    def parse_details(self, response):
        item = ScrapyEplanningItem()
        agents_button = response.xpath('//input[@title="Show Agents Popup"]/@style').get()
        if 'display: inline;  visibility: visible;' in agents_button:
            item['name'] = parse_table_info(response, 'Name')
            item['number'] = parse_table_info(response, 'Phone')
            item['fax'] = parse_table_info(response, 'Fax')
            item['e_mail'] = parse_table_info(response, 'e-mail')

            address_first = parse_table_info(response, 'Address')
            item['all_addresses'] = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').getall()[:3]
            item['all_addresses'].append(address_first)

            yield item

        else:
            self.logger.info(f'No AGENTS button on current page: {response}')
