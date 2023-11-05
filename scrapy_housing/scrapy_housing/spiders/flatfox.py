from typing import Generator
import scrapy

# Scrapy tutorial: https://towardsdatascience.com/web-scraping-with-scrapy-theoretical-understanding-f8639a25d9cd
# XPath tutorial: https://www.blog.datahut.co/post/xpath-for-web-scraping-step-by-step-tutorial


class FlatfoxSpider(scrapy.Spider):
    name = "flatfox"
    # To avoid going off to other websites
    allowed_domains = ["flatfox.ch"]
    start_urls = [
        # "https://flatfox.ch",
        "https://flatfox.ch/en/search/?east=8.625334&north=47.455518&query=Z%C3%BCrich&south=47.299348&west=8.447982",
        # "https://flatfox.ch/en/search/?query=Z%C3%BCrich",
    ]
    filename = "flatfox_ch_zurich_full_coordinates"

    def start_requests(self) -> Generator[scrapy.Request, None, None]:
        """
        This can be used to generate the requests instead of using `start_urls`
        """
        urls = ["http://example.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        with open(f"{self.filename}.html", "w+") as f:
            f.write(response.body.decode())
        print(response)
        print(response.body)
        print("\nHELLO\n")
