import scrapy
import pymongo
from .xpath_selectors import PAGINATION, VACANCY, VACANCY_DATA, COMPANY_DATA
from ..loaders import HhVacancyLoader, HhCompanyLoader


class HeadhunterSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['vladivostok.hh.ru']
    start_urls = ['https://vladivostok.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.xpath(selector_str):
            yield response.follow(a_link, callback=callback)

    def parse(self, response):
        for item in (PAGINATION, VACANCY):
            yield from self._get_follow(response, item['selector'], getattr(self, item['callback']))

    def vacancy_parse(self, response):
        loader = HhVacancyLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in VACANCY_DATA.items():
            loader.add_xpath(key, selector)
            if key == 'company_url':
                yield from self._get_follow(response, selector, getattr(self, 'company_parse'))
        yield loader.load_item()

    def company_parse(self, response):
        print(1)
        loader = HhCompanyLoader(response=response)
        loader.add_value('url', response.url)
        for key, selector in COMPANY_DATA.items():
            loader.add_xpath(key, selector)
        yield loader.load_item()


