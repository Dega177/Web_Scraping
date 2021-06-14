from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose


def create_company_link(link_str):
    return urljoin('https://vladivostok.hh.ru/', link_str)


def create_description(description):
    result = '\n'.join(description)
    return result.replace('\xa0', '')


def clear_salary(salary):
    return salary.replace('\xa0', '')


def create_company_name(company_name):
    result = set(company_name)
    result = ' '.join(result)
    for value in ['\xa0', '  ']:
        result = result.replace(value, '')
    return result


class HhVacancyLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_in = MapCompose(clear_salary)
    salary_out = TakeFirst()
    description_in = create_description
    description_out = TakeFirst()
    company_url_in = MapCompose(create_company_link)
    company_url_out = TakeFirst()


class HhCompanyLoader(ItemLoader):
    default_item_class = dict
    name_in = create_company_name
    name_out = TakeFirst()
    company_site_out = TakeFirst()
    description_in = create_description
    description_out = TakeFirst()