from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from re import search

class Gatherer:
    'Takes a Magiccardsinfo set, id and returns the Gatherer id'
    
    def __init__(self, id=None, set=None):
        self.url = 'http://magiccards.info/%s/en/%s.html' % (set, id)
        self.__request()
        
    def __request(self):
        'Make a request to the Magiccard Info page'
        card = urlopen(self.url).read()
        m = search('multiverseid=([\d]+)', card)
        if m:
            self.gatherer_id = m.group(1)
        else:
            raise Exception('unable to find multiverseid in %s' % self.url)

    def getGathererId(self):
        'Returns a multiverseid for a card'
        return self.gatherer_id
