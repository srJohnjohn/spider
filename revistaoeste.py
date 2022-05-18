import scrapy
from scrapy.crawler import CrawlerProcess

class RevistaOesteScraper(scrapy.Spider):
    name = 'revista_oeste'

    headers = {
        'user-agent': ''
    }

    base_url =  'https://revistaoeste.com/colunista/rodrigo-constantino/' #'https://revistaoeste.com/'

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, headers=self.headers, callback=self.parse_newl)
        

    
    # def parse(self, res):
    #     menu = res.css('li.menu-item a::attr(href)').getall()
    #     for topic in menu:
    #         #link = topic.css('a::attr(href)').get()
    #         print(topic)

    def parse_newl(self, res):
        for artigo in res.css('article'):
            title = artigo.css('h2 a::text').get()
            link = artigo.css('a').attrib['href']
            resumo = artigo.css('div.entry-summary p::text').get()

            # print(title)
            # print(link)
            # print(resumo)
            # print('*************\n\n\n')

            yield{
                'title' : title,
                'link' : link,
                'resumo' : resumo,
            }
    
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(RevistaOesteScraper)
    process.start()



