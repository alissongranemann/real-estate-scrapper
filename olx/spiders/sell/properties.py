from scrapy import Spider, Request
from scrapy.loader import ItemLoader

from urllib.parse import urlparse
from olx.spiders.sell.items import Property
from olx.spiders.sell.loaders import PropertyLoader

class PropertiesSpider(Spider):
    name = "properties"

    def __init__(self, *args, **kwargs):
        self.start_urls = [
            "https://sc.olx.com.br/florianopolis-e-regiao/centro/imoveis/venda?sf=1"
        ]
        self.allowed_domains = map(lambda x: urlparse(x).netloc, self.start_urls)

    def parse(self, response):
        listing = response.css("div.section_listing")
        announcements_section = listing.css("div.section_OLXad-list")
        announcements_items = announcements_section.css("li")
        pagination = listing.css("div.module_pagination")

        for item in announcements_items:
            loader = PropertyLoader(item=Property(), selector=item)
            loader.add_css('id', 'li::attr(data-list_id)')
            loader.add_css('area', 'p.detail-specific::text')
            loader.add_css('price', 'p.OLXad-list-price::text')
            yield loader.load_item()

        # next_page = pagination.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     yield scrapy.Request(next_page, callback=self.parse)
