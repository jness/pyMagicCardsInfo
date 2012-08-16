from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from re import search
import unidecode
        
class Card:
    'Get a complete set'
    
    def __init__(self, set=None):
        self.url = 'http://magiccards.info/%s/en.html' % set
        self.__set()
        self.__card_tds()
        self.__cards()
        
    def __set(self):
        'Request the set from magiccards.info'
        self.set = urlopen(self.url).read()
        
    def __card_tds(self):
        'Use BeautifulSoup to get all card tr blocks'
        soup = BeautifulSoup(self.set)
        self.card_tds = soup.findAll('tr', {'class': ['odd', 'even']})
        
    def __cards(self):
        'Extract data from the card td blocks'
        self.cards = {}
        for card in self.card_tds:
            card_tds = card.findAll('td')
           
            # extract the data from the td structure
            id = card_tds[0].text
            card_name = card_tds[1].text
            cost = card_tds[3].text
            rarity = card_tds[4].text
            artist = card_tds[5].text
            
            # check if card has a power / toughness
            m = search('[\*0-9]*/[\*0-9]', card_tds[2].text)
            if m:
                pow = m.group(0)
                power = m.group(0).split('/')[0]
                toughness = m.group(0).split('/')[1]
                type = card_tds[2].text.replace(' %s' % pow, '')
                type = type.replace(u'\u2014' ,'-')
            else:
                power = None
                toughness = None
                type = card_tds[2].text.replace(u'\u2014' ,'-')
                
            # type all non values alike
            if not cost:
                cost = None
                
            # construct a dict
            self.cards[id] = dict(card_id=id, card_name=card_name, cost=cost,
                                  rarity=rarity, artist=artist, type=type,
                                  power=power, toughness=toughness)
            
    def __searchNames(self, name=None):
        'Return all ids matching a name'
        name = name.lower()
        ids = [ i for i in self.cards if name in self.cards[i]['card_name'].lower() ]
        if not ids:
            # try in ASCII
            ids = [ i for i in self.cards if name in unidecode.unidecode(self.cards[i]['card_name']).lower() ]
        return ids

    def __search(self, name=None):
        'Return a single ids for matching name'
        name = name.lower()
        id = [ i for i in self.cards if name == self.cards[i]['card_name'].lower() ]
        if not id:
            # try in ASCII
            id = [ i for i in self.cards if name == unidecode.unidecode(self.cards[i]['card_name']).lower() ]
        return id
    
    def getCards(self):
        'Return a dict of card in the set'
        return self.cards
    
    def getCard(self, name=None):
        'Return a dict of a specific card'
        name = name.replace('AEther', u'\xc6ther')
        name = name.replace('Aether', u'\xc6ther')
        id = self.__search(name=name)
        if len(id) == 0:
            raise Exception('%s not found in set' % name)
        if len(id) > 1:
            # sets with duplicate cards will also fail here
            names = []
            for i in id:
                names.append(self.cards[i]['card_name'])
            # if names match just return first object
            if len(set(names)) != 1:
                raise Exception('More than 1 match found for %s' % name)
        
        # no exceptions means we return
        return self.cards[id[0]]
    
    def searchCards(self, name=None):
        'Return a list of dicts per search name'
        cards = []
        name = name.replace('AEther', u'\xc6ther')
        name = name.replace('Aether', u'\xc6ther')
        ids = self.__searchNames(name=name)
        for id in ids:
            cards.append(self.cards[id])
        return cards

