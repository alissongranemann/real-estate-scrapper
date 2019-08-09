from scrapy import Spider, Request
from scrapy.loader import ItemLoader

from urllib.parse import urlparse
from olx.spiders.items import Property
from olx.spiders.loaders import PropertyLoader


class SellPropertiesSpider(Spider):
    name = "sell_properties"

    def __init__(self, state=None, **kwargs):
        super().__init__(**kwargs)
        if state is None:
            raise ValueError("%s must have a state" % self.name)
        self.start_urls = [
            f"https://{state}.olx.com.br/imoveis/venda"
        ]

    #     self.allowed_domains = map(lambda x: urlparse(x).netloc, self.start_urls)

    def parse(self, response):
        menu_list = response.css("div.linkshelf-tabs-content ul.list")
        macro_regions = menu_list.css("li.item")
        for region in macro_regions:
            url = region.css("p.text a::attr(href)").get()
            yield response.follow(url=url, callback=self.micro_regions)
        
    
    def micro_regions(self, response):
        menu = response.css("div.linkshelf-tabs-content")
        micro_regions = menu.css("div.linkshelf-zone ul.list li.item a.link")
        for micro_region in micro_regions:
            url = micro_region.css("a::attr(href)").get()
            yield response.follow(url=url, callback=self.parse_list)


    def parse_list(self, response):
        listing = response.css("div.section_listing")
        announcements_section = listing.css("div.section_OLXad-list")
        announcements_items = announcements_section.css("li")

        for item in announcements_items:
            loader = PropertyLoader(item=Property(), selector=item)
            loader.add_css('id', 'li::attr(data-list_id)')
            loader.add_css('area', 'p.detail-specific::text')
            loader.add_css('price', 'p.OLXad-list-price::text')
            yield loader.load_item()

        next_page = listing.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield Request(next_page, callback=self.parse)
