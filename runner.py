from scrapy.cmdline import execute

# VSCode debug helper

execute(["scrapy", "runspider", "./olx/spiders/properties/sell.py", "-a", "state=sc"])
