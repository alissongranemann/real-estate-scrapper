import scrapy

class Property(scrapy.Item):
    id = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
