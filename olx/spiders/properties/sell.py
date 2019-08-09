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
        self.start_urls = [f"https://{state}.olx.com.br/imoveis/venda"]

    def parse(self, response):
        macro_regions = response.css("div.linkshelf-tabs-content ul.list li.item")
        for region in macro_regions:
            url = region.css("p.text a::attr(href)").get()
            return response.follow(url=url, callback=self.parse_micro_regions)

    def parse_micro_regions(self, response):
        micro_regions = response.css(
            "div.linkshelf-tabs-content div.linkshelf-zone ul.list li.item a.link"
        )
        for micro_region in micro_regions:
            url = micro_region.css("a::attr(href)").get()
            return response.follow(url=url, callback=self.parse_properties_list)

    def parse_properties_list(self, response):
        listing = response.css("div.section_listing")
        announcements_items = listing.css("div.section_OLXad-list li.item a")

        for item in announcements_items:
            url = item.css("a::attr(href)").get()
            yield response.follow(url=url, callback=self.parse_property)

        # next_page = listing.css("li.next a::attr(href)").get()
        # if next_page is not None:
        #     yield Request(next_page, callback=self.parse_properties_list)

    def parse_property(self, response):
        loader = PropertyLoader(item=Property(), response=response)
        loader.add_css("id", "div.OLXad-id strong.description::text")
        loader.add_xpath(
            "area",
            "//div[contains(@class, 'OLXad-detail')]//ul//li[@class='item']/p/strong[contains(text(), 'm²')]/text()",
        )
        loader.add_xpath(
            "cep",
            "//div[contains(@class, 'OLXad-location')]//ul//li[@class='item']/p/span[contains(text(), 'CEP')]/following-sibling::strong/text()",
        )
        loader.add_css("price", "h3.price span.actual-price::text")
        yield loader.load_item()
