from scrapy import Selector
from urllib.parse import urljoin
import re
import requests


def create_title(title):
    result = ' '.join(title).replace('\xa0', ' ')
    return result


def create_address(address):
    result = ' '.join(address).replace('\n ', '')
    return result


def get_characteristics(item):
    selector = Selector(text=item)
    data = {
        'name': selector.xpath('//span[@class="item-params-label"]/text()').get().strip(),
        'value': selector.xpath('//li/text()').extract()[1].strip()
    }
    return data


def create_author_url(url):
    author_id = url.split('?')[0]
    return urljoin('https://www.avito.ru', author_id)


def get_phone(id_str):
    apartment_id = re.search(r'\d.*\d', id_str).group()
    url = f'https://m.avito.ru/api/1/items/{apartment_id}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
    response = requests.get(url)
    data = response.json()
    phone = re.search(r'.{11}$', data['result']['action']['uri']).group()
    return phone


