from scrapy.exceptions import DropItem


class EmptySellPropertyPipeline(object):
    def process_item(self, item, spider):
        if not item or item.get("area") is None or item.get("price") is None:
            raise DropItem(f"Invalid or empty item found: {item}")
        return item
