from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from .processors import create_title, create_address, get_characteristics, create_author_url, get_phone


class AvitoApartmentLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_in = create_title
    title_out = TakeFirst()
    price_out = TakeFirst()
    address_in = create_address
    address_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)
    author_in = MapCompose(create_author_url)
    author_out = TakeFirst()
    phone_in = MapCompose(get_phone)
    phone_out = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
