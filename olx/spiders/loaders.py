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


def remove_inner_spaces(detail):
    return "".join(detail.split())


def get_area(raw_area):
    regex = re.compile(r".*\|([0-9]+)m²\|.*")
    match = regex.match(raw_area)
    if match:
        return int(match.group(1))


class PropertyLoader(ItemLoader):

    default_output_processor = TakeFirst()
    area_out = Compose(TakeFirst(), str.strip, remove_inner_spaces, get_area)
    price_out = Compose(TakeFirst(), str.strip, get_price)
