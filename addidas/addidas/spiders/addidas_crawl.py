import scrapy


class AddidasCrawlSpider(scrapy.Spider):
    name = 'addidas_crawl'
    allowed_domains = ['addidas.com']
    start_urls = ['http://addidas.com/']

    def parse(self, response):
        pass
