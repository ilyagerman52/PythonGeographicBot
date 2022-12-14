import scrapy
from spider_geooge.items import SpiderGeoogeItem

class GeoogespiderSpider(scrapy.Spider):
    name = 'GeoOgeSpider'

    def start_requests(self):
        print("еcли парсим 17ый номер введи 1, если 18ый что угодно другое")
        a = input()
        if a == "1":
            for page in range(1, 6):
                url = f"https://geo-ege.sdamgia.ru/search?search=определите%20страну%20по%20описанию&cb=1&body=3&solution=1&text=2&keywords=10&attr[]=177&no_attr[]=189&page={page}"
                yield scrapy.Request(url, callback=self.parse_pages)
        else:
            for page in range(1, 6):
                url = f"https://geo-ege.sdamgia.ru/search?search=определите%20регион%20по%20описанию&cb=1&body=3&solution=1&text=2&keywords=10&no_attr[]=177&page={page}"
                yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for href in response.xpath('//div/div/span[contains(@class, "prob_nums")]/a/text()').extract():
            url = f"https://geo-ege.sdamgia.ru/problem?id={href}"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        items = SpiderGeoogeItem()
        question = response.xpath('//div[contains(@class, "pbody")]/p/text()').extract()
        answer = response.xpath('//div[contains(@class, "answer")]/span/text()').extract()
        items["question"] = ''.join(question).strip()
        items["answer"] = ' '.join(answer)[7:].strip()
        yield items


