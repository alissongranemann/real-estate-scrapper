import requests
import os
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings


class SellPropertyPipeline(object):
    def open_spider(self, spider):
        self.API_URL = spider.settings.get("REAL_ESTATE_API")

    def process_item(self, item, spider):
        if not item or item.get("area") is None or item.get("price") is None:
            raise DropItem(f"Invalid or empty item found: {item}")

        r = requests.post(self.API_URL, json=dict(item))
        if r.status_code != 201:
            # id = item.get("id")
            raise DropItem(f"Failed to post item - HTTP {r.status_code}")
        return item
