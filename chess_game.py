import scrapy
from scrapy.crawler import CrawlerProcess

class ChessGameScraper(scrapy.Spider):
    name = 'chess_game'

    headers = {
        'user-agent': ''
    }

    base_url = 'https://lichess.org/@/Kingscrusher-YouTube/search'


    def start_requests(self):
        key_id = 1584694629328
        
        # loop over pages
        for page in range(1, 5):   # set max pages up to 1500 up to
            next_page = self.base_url + '?page=' + str(page) + '&perf=2&sort.field=d&sort.order=desc&_=' + str(key_id)
            #print(next_page)
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse_game_list)
            key_id += 1

    def parse_game_list(self, res):
        #extract gamelinks
        games = res.css('a.game-row__overlay::attr(href)').getall()

        #loop over game links
        for game in games:
            yield res.follow(url=game, headers=self.headers, callback=self.parse_game)
            break
            print('um novo game\n')
            print(game)

    def parse_game(self, res):
        pgn = res.css('div.pgn::text').get()
        print(pgn)


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ChessGameScraper)
    process.start()