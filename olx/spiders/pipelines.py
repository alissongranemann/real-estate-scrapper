from scrapy.exceptions import DropItem


class EmptySellPropertyPipeline(object):
    def process_item(self, item, spider):
        if item["id"] is None:
            raise DropItem(f"Empty item found: {item}")
        return item
