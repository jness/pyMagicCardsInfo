from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from re import search

class Identifiers:
    'Takes a Magiccardsinfo set, id and returns the Gatherer and TCG id'
    
    def __init__(self, id=None, set=None):
        self.url = 'http://magiccards.info/%s/en/%s.html' % (set, id)
        self.__request()
        
    def __request(self):
        'Make a request to the Magiccard Info page'
        self.card = urlopen(self.url).read()
        
    def getGathererId(self):
        'Returns a multiverseid for a card'
        m = search('multiverseid=([\d]+)', self.card)
        if m:
            self.gatherer_id = m.group(1)
            return self.gatherer_id
        else:
            raise Exception('unable to find multiverseid in %s' % self.url)

    def getTCGPlayerId(self):
        'Returns a tcgplayer id for a card'
        m = search('MAGCINFO&amp;sid=([\d]*)', self.card)
        if m:
            self.tcgplayer_id = m.group(1)
            return self.tcgplayer_id
        else:
            raise Exception('unable to find tcgplayer id in %s' % self.url)