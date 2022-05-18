from tracemalloc import start
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesScraper(scrapy.Spider):
    name = 'quotes'

    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        quotes = response.css('div.quote')
        print('..........................')
        span = quotes.css('span.text::text').getall()
        for quote in response.css('div.quote'):
            yield{
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }


process = CrawlerProcess()
process.crawl(QuotesScraper)
process.start()