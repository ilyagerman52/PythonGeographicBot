import scrapy


class SpiderGeoogeItem(scrapy.Item):
    question = scrapy.Field()
    answer = scrapy.Field()
    pass
