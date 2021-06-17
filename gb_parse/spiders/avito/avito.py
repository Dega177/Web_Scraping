import scrapy
from .xpath_selectors import PAGINATION, APARTMENT, APARTMENT_DATA, CATEGORY
from .loaders import AvitoApartmentLoader


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['www.avito.ru']
    start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam-ASgBAgICAUSSA8YQ']

    def _get_follow(self, response, xpath, callback):
        for url in response.xpath(xpath):
            yield response.follow(url, callback=callback)

    def parse(self, response):
        for item in (PAGINATION, APARTMENT):
            yield from self._get_follow(response, item["selector"], getattr(self, item["callback"]))

    def apartment_parse(self, response):
        loader = AvitoApartmentLoader(response=response)
        for key, selector in APARTMENT_DATA.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()
        yield from self._get_follow(response, CATEGORY["selector"], getattr(self, CATEGORY["callback"]))







