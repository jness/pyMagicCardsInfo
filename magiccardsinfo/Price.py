from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from re import search

class Price:
    'Takes a Magiccardsinfo set, id and returns the Low, Avg and High Prices'
    
    def __init__(self, id=None, set=None):
        self.url = 'http://magiccards.info/%s/en/%s.html' % (set, id)
        self.__request()
        self.__request_tcg()
        self.__prices()
        
    def __request(self):
        'Make a request to the Magiccard Info page'
        card = urlopen(self.url).read()
        m = search('MAGCINFO&amp;sid=([\d]*)', card)
        if m:
            self.tcgplayer_id = m.group(1)
        else:
            raise Exception('unable to find tcgplayer id in %s' % self.url)
            
    def __request_tcg(self):
        'Make a request to the TCGPlayer page'
        self.tcgurl = 'http://store.tcgplayer.com/Product.aspx?id=%s' % \
                       self.tcgplayer_id
        self.card = urlopen(self.tcgurl).read()
        
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