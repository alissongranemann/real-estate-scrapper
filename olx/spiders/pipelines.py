from scrapy.exceptions import DropItem


class EmptySellPropertyPipeline(object):
    def process_item(self, item, spider):
        if item["area"] is None or item["price"]:
            raise DropItem(f"Empty item found: {item}")
        return item
