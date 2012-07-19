from urllib2 import urlopen
from re import compile

class Set:
    'Simple class for getting sets from the magiccards.info sitemap'
    
    def __init__(self):
        self.url = 'http://magiccards.info/sitemap.html'
        self.__sitemap()
        self.__sets()
    
    def __sitemap(self):
        'Request the sitemap page from magiccards.info'
        self.sitemap = urlopen(self.url).read()
        
    def __sets(self):
        'Use regular expression to get sets'
        expr = '<a href="/([\w]*)/en.html">([\w :\'\.\-/"]*)</a> <small'
        self.sets = compile(expr).findall(self.sitemap)

    def getSets(self):
        'Return a dict of sets found on the magiccards.info sitemap'
        return dict(self.sets)