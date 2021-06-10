import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.css(selector_str):
            url = a_link.attrib['href']
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow(
            response,
            '.TransportMainFilters_brandsList__2tIkv a.blackLink',
            self.brand_parse
        )

    def brand_parse(self, response):

        selectors = (
            ('div.Paginator_block__2XAPy a.Paginator_button__u1e7D', self.brand_parse),
            ('article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu', self.car_parse)
        )

        for selector, callback in selectors:
            yield from self._get_follow(
                response,
                selector,
                callback
            )

    def car_parse(self, response):
        print(1)
        data = {
            'title': response.css('div.AdvertCard_advertTitle__1S1Ak::text').extract_first(),
            'price': response.css('div.AdvertCard_price__3dDCr::text').extract_first().replace('\u2009', ' '),
            'description': response.css(
                'div.AdvertCard_descriptionWrap__17EU3 div.AdvertCard_descriptionInner__KnuRi::text'
            ).extract_first(),
            'equipment': response.css(
                'div.AdvertEquipment_equipmentSectionList__3r5xo div.AdvertEquipment_equipmentItem__Jk5c4::text'
            ).extract(),
            'img': [img.attrib['src'] for img in
                    response.css('div.PhotoGallery_photoWrapper__3m7yM img.PhotoGallery_photoImage__2mHGn')],
            'specs': dict(
                zip(
                    response.css('div.AdvertSpecs_row__ljPcX div.AdvertSpecs_label__2JHnS::text').extract(),
                    response.css('div.AdvertSpecs_row__ljPcX div.AdvertSpecs_data__xK2Qx::text').extract()
                )
            )
        }

        return data
