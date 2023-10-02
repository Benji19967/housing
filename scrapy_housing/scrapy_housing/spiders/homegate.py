import scrapy


class HomegateSpider(scrapy.Spider):
    name = "homegate"
    allowed_domains = ["homegate.ch"]
    start_urls = ["https://homegate.ch/rent"]

    def parse(self, response):
        print(response.url)
        print(response.body)
