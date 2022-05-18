import scrapy 
import time
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

class Onthemarket(scrapy.Spider):
    name = 'kohlsmarket'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'kohls.csv'
    }

    header = {
        'user-agent': ''
        
    }

    def start_requests(self):
        print('.............................')
        urls= 'https://www.kohls.com/catalog/fathers-day.jsp?CN=Occasion:Father%27s%20Day+Price:%2410%20to%20%2425&BL=y&icid=dadsdaygiftshop-PB1-25&sks=true&kls_sbp=02554466659989310275352623798292254384&PPP=48&WS=0&S=1'
        yield scrapy.Request(url=urls, headers=self.header, callback=self.parse)

    def parse(self, response):
        # self.log('status' + str(response.status))
        # print('status' + str(response.status))
        print('...........................')
        # with open('kohls.html', 'w') as html_file:
        #     html_file.write(response.text)
        html = ''
        with open('kohls.html', 'r')as html_file:
            for line in html_file.read():
                html += line
        

        #Selector(text=html).xpath('').get()
        response = Selector(text=html)
        for card in response.css('li.products_grid'):
            yield {
                'title': card.css('div.prod_nameBlock').css('p::text').get().strip(),
                'price': card.css('span.prod_price_amount::text').get(), #.encode('ascii', 'ignore').decode('utf-8').strip(),
                'color': card.css('span.colorSwatch').css('a::attr(title)').extract(),
            #     'drecription': card.css('li.otm-ListItemOtmBullet::text').getall(),
            #     'telephon': card.css('div.otm-Telephone::text').get(),
            #     'image_urls': card.css('picture').css('img::attr(src)').getall()
            }
            # print(card.css('span.colorSwatch').css('a::attr(title)').extract())
            print('.....................')
            #print(json.dumps(item, indent=2))    
            #print(card)
        #time.sleep(2)
        ###### NEXT PAGE #######
        # next_page = response.css('a.order-last::attr(href)').get()
        # print(next_page)
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     #next_page = 'https://www.onthemarket.com' + next_page
        #     print(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
        #print(response.css('li.otm-PropertyCard').css('a::text').getall())


#Onthemarket.parse(Onthemarket, '')

process = CrawlerProcess()
process.crawl(Onthemarket)
process.start()
