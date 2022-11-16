import scrapy


class AddidasCrawlSpider(scrapy.Spider):
    name = 'addidas_crawl'
    allowed_domains = ['shop.adidas.jp']
    start_urls = ['https://shop.adidas.jp/men/']

    def parse(self, response):
        pass
