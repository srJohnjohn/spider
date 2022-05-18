import scrapy

class whiskeySpider(scrapy.Spider):
    name = 'whisky'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky?item_availability=In+Stock']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            print('lnk')
            name = products.css('a.product-item-link::text').get()
            print(name)
            price = products.css('span.price::text').get().replace('£', '')
            link = products.css('a.product-item-link').attrib['href']
            try:
                yield{
                    'name': name,
                    'price': price,
                    'link': link,
                }
            except:
                yield{
                    'name': products.css('a.porduct-item-link::text').get(),
                    'price': 'sold out',
                    'link': link,
                }
            
        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
