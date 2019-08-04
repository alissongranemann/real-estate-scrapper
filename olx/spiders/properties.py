import scrapy
import locale
import re


class PropertiesSpider(scrapy.Spider):
    name = "properties"
    start_urls = [
        "https://sc.olx.com.br/florianopolis-e-regiao/centro/imoveis/venda?sf=1"
    ]

    def parse(self, response):
        listing = response.css("div.section_listing")
        announcements_section = listing.css("div.section_OLXad-list")
        announcements_items = announcements_section.css("li")
        pagination = listing.css("div.module_pagination")

        for item in announcements_items:
            item_id = item.css("li::attr(data-list_id)")
            detail = item.css("p.detail-specific::text")
            price_text = item.css("p.OLXad-list-price::text")
            price = self.get_price(price_text.get())
            area = self.get_area(detail.get())

            if area and price:
                yield {"item_id": item_id.get(), "area": area, "price": price}

        next_page = pagination.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)

    def get_area(self, detail):
        if detail:
            regex = re.compile(r".*\|([0-9]+)m²\|.*")
            area = detail.strip()
            match = regex.match("".join(area.split()))
            if match:
                return int(match.group(1))
        return None

    def get_price(self, raw_price):
        if not raw_price:
            return None
        raw_price = raw_price.strip()
        locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")
        conv = locale.localeconv()
        raw_numbers = raw_price.strip(conv["currency_symbol"])
        return locale.atof(raw_numbers)
