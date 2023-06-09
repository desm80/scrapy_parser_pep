from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://{}/'.format(*allowed_domains)]

    def parse(self, response):
        """Парсинг ссылок на странички с конкретным Pep."""
        table = response.css('#numerical-index')
        links = table.css('td > a::attr(href)').getall()
        for link in links:
            pep_url = urljoin(*self.start_urls, link + '/')
            yield response.follow(pep_url, callback=self.parse_pep)

    def parse_pep(self, response):
        """Парсинг информации о статусе Pep и его названия."""
        name = response.css('#pep-content > h1::text').get()
        data = {
            'number': int(list(name.split(' '))[1]),
            'name': name,
            'status': response.css('abbr::text').get(),
        }
        yield PepParseItem(data)
