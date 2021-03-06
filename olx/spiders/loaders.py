import locale
import re

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose


def get_price(raw_price):
    raw_price = raw_price.strip()
    locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
    conv = locale.localeconv()
    raw_numbers = raw_price.strip(conv["currency_symbol"])
    return locale.atof(raw_numbers)


def get_area(raw_area):
    regex = re.compile(r"([0-9]+)\s?m²")
    match = regex.match(raw_area)
    if match:
        return int(match.group(1))


class PropertyLoader(ItemLoader):

    default_output_processor = Compose(TakeFirst(), str.strip)
    area_out = Compose(TakeFirst(), str.strip, get_area)
    price_out = Compose(TakeFirst(), str.strip, get_price)

    def load_item(self):
        item = self.item
        for field_name in tuple(self._values):
            value = self.get_output_value(field_name)
            if value is not None:
                item[field_name] = value

        return item
