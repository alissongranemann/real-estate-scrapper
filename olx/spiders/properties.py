import scrapy


class PropertiesSpider(scrapy.Spider):
    name = "properties"

    start_urls = [
        "https://sc.olx.com.br/imoveis/venda?sf=1",
    ]

    def parse(self, response):
        announcements_section = response.css(
            "div.section_OLXad-list"
        )

        announcements_items = announcements_section.css("li")
        for item in announcements_items:
            title = item.css("h2.OLXad-list-title::text")
            detail = item.css("p.detail-specific::text")
            price = item.css("p.OLXad-list-price::text")
            area = None
            if detail:
                detail_text = detail.get().strip()
                if "m²" in detail_text:
                    first = detail_text.find("|") + 1
                    detail_text = detail_text[first:]
                    area = detail_text[: detail_text.find("|")].strip()
            if area and price:
                yield {
                    "title": title.get().strip(),
                    "area": area,
                    "price": price.get().strip(),
                }
