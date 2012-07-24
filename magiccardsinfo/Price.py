from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from re import search

class Price:
    'Takes a TCGPlayer ID and gets the low, avg, and high prices'
    
    def __init__(self, id=None):
        self.url = 'http://store.tcgplayer.com/Product.aspx?id=%s' % id
        self.__request()
        self.__prices()
        
    def __request(self):
        'Make a request to the TCGPlayer page'
        self.card = urlopen(self.url).read()
        
    def __prices(self):
        'Pull the prices from the td structure'
        soup = BeautifulSoup(self.card)
        prices = soup.findAll('td', {'class': ['low', 'avg', 'high']})
        if len(prices) == 3:
            self.low = prices[0].text
            self.avg = prices[1].text
            self.high = prices[2].text
        else:
            raise Exception('3 prices not found on page %s' % self.url)
            
        # get card name
        names = soup.findAll('div', {'id': 'cardName'})
        if len(names) == 1:
            self.card_name = names[0].text
        else:
            raise Exception('Failed to pull card name on page %s' % self.url)

    def getPrices(self):
        'Returns a dict of low, avg, and high'
        return dict(low=self.low, avg=self.avg, high=self.high,
                    card_name = self.card_name)