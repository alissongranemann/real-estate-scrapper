from scrapy.exceptions import DropItem
import requests


class SellPropertyPipeline(object):
    def process_item(self, item, spider):
        if not item or item.get("area") is None or item.get("price") is None:
            raise DropItem(f"Invalid or empty item found: {item}")
        r = requests.post("http://localhost:5000/api/v1/properties", json=dict(item))
        if r.status_code != 201:
            # id = item.get("id")
            raise DropItem(f"Failed to post item.")
        return item
