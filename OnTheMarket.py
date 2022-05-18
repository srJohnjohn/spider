import scrapy 
import time
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

class Onthemarket(scrapy.Spider):
    name = 'onthemarket'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'onthemarket.csv'
    }

    header = {
        'user-agent': ''
        
    }

    def start_requests(self):
        print('.............................')
        urls= 'https://www.onthemarket.com/for-sale/property/london/'
        yield scrapy.Request(url=urls, headers=self.header, callback=self.parse)

    def parse(self, response):
        # self.log('status' + str(response.status))
        # print('status' + str(response.status))
        # print('...........................')
        # with open('res.html', 'w') as html_file:
        #     html_file.write(response.text)
        # html = ''
        # with open('res.html', 'r')as html_file:
        #     for line in html_file.read():
        #         html += line
        

        #Selector(text=html).xpath('').get()
        #response = Selector(text=html)
        for card in response.css('li.otm-PropertyCard'):
            yield {
                'title': card.css('span.title').css('a::text').get(),
                'price': card.css('div.price::text').get(), #.encode('ascii', 'ignore').decode('utf-8').strip(),
                'address': card.css('span.address').css('a::text').get(),
                'drecription': card.css('li.otm-ListItemOtmBullet::text').getall(),
                'telephon': card.css('div.otm-Telephone::text').get(),
                'image_urls': card.css('picture').css('img::attr(src)').getall()
            }
            #print(card.css('span.address').css('a::text').getall())
            print('.....................')
            #print(json.dumps(item, indent=2))    
            #print(card)
        time.sleep(2)
        next_page = response.css('a.order-last::attr(href)').get()
        print(next_page)
        if next_page is not None:
            next_page = response.urljoin(next_page)
            #next_page = 'https://www.onthemarket.com' + next_page
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        #print(response.css('li.otm-PropertyCard').css('a::text').getall())


#Onthemarket.parse(Onthemarket, '')

process = CrawlerProcess()
process.crawl(Onthemarket)
process.start()

