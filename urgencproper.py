import scrapy
from scrapy import selector
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from w3lib.url import safe_download_url

class PropertyLinkExtractor(scrapy.Spider):
    name = 'argenprop'
    start_urls = ['https://www.argenprop.com/']
    base_url = 'https://www.argenprop.com/'

    headers = {
        'user-agent': ''
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.extract_links
        )

    def extract_links(self, response):
        with open('res.html') as f:
            response = Selector(text=f.read())
            # print(response.text)
            # f.write(response.text)
        
        sale_links = response.css('div[class="suggested__search"]')
        sale_links = sale_links.css('a[href*=venta]::attr(href)').getall()
        print(len(sale_links))

        rent_links = response.css('div[class="suggested__search"]')
        rent_links = rent_links.css('a[href*=alquiler]::attr(href)').getall()
        print(rent_links)
            
        self.store_links('residential_sale.txt', sale_links)
        self.store_links('residential_rent.txt', rent_links)
        

    def store_links(selff, filename, links):
        with open(filename, 'w') as f:
            for link in links:
                f.write(link + '\n')

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(PropertyLinkExtractor)
    process.start()

    #PropertyLinkExtractor.extract_links(PropertyLinkExtractor, '')