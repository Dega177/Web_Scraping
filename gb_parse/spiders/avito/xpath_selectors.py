PAGINATION = {
    'selector': '//div[contains(@class, "pagination-pages")]/a[@class="pagination-page"]/@href',
    'callback': 'parse'
}

APARTMENT = {
    'selector': '//div[@data-marker="catalog-serp"]//a[@data-marker="item-title"]/@href',
    'callback': 'apartment_parse'
}

APARTMENT_DATA = {
    'title': '//title/text()',
    'price': '//div[@id="price-value"]//span[@itemprop="price"]/@content',
    'address': '//div[@itemprop="address"]//text()',
    'characteristics': '//div[@class="item-params"]//li[@class="item-params-list-item"]',
    'author': '//div[@data-marker="seller-info/name"]/a/@href',
    'phone': '//div[@id="abuse"]/@data-abuse'
}

CATEGORY = {
    'selector': '//div[@class="item-navigation "]//meta[@content > 4]/../a[@itemprop="item"]/@href',
    'callback': 'parse'
}