import requests
from bs4 import BeautifulSoup


URL = "https://sc.olx.com.br/imoveis/venda?sf=1"


class OlxScrapper:
    def scrap():
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, "html.parser")
        announcements_section = (
            soup.find(class_="page_listing")
            .find(class_="section_listing")
            .find(class_="section_OLXad-list")
        )
        announcements_items = announcements_section.find_all("li")
        for item in announcements_items:
            # title = item.find("h2", class_="OLXad-list-title")
            detail = item.find("p", class_="detail-specific")
            price = item.find("p", class_="OLXad-list-price")
            area = None
            if detail:
                detail_text = detail.text.strip()
                if "m²" in detail_text:
                    first = detail_text.find("|") + 1
                    detail_text = detail_text[first:]
                    area = detail_text[: detail_text.find("|")].strip()
            if area and price:
                print(f"Area: {area} - Price: {price.text.strip()}")

