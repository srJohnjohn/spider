import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class PropertyLinkExtrator(scrapy.Spider):
    name = 'argenpro'

    url_base = 'http://www.argenprop.com/'

    headers = {
        'user-agent': ''#
    }

    def start_requests(self):
        '''make http get resquest to target url'''
        yield scrapy.Request(
            url=self.url_base,
            headers=self.headers,
            callback=self.extrat_links
        )

    def extrat_links(self, response):
        # with open('res.html') as f:
        #     f.write(response.text)
        #     response = Selector(text=f.read())
        # response.css('div.suggested__search')
        print(response.css('div.suggested__search'))
        print("...........................")
        sale_links = response.css('div.suggested_search')
        print(response.css('a[href*=venta]::attr(href)').getall())
        print("...........................")

        sale_links = response.css('a[href*=venta]::attr(href)').getall()
        for sl in sale_links:
            print (sl)

        self.store_links('residential_sale.txt', sale_links)
        # print(sale_links)

    # store links to file
    def store_links(self, filename, links):
        with open(filename, 'w') as f:
            for link in links:
                print(link)
                f.write(link + '\n')




if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(PropertyLinkExtrator)
    process.start() 

    #PropertyLinkExtrator.extrat_links(PropertyLinkExtrator, '')