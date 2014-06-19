class MarketDetails(object):

    def __init__(self, identity, marketname, address, googlelink, products, schedule):
        self.identity = identity
        self.marketname = marketname
        self.address = address
        self.googlelink = googlelink
        self.products = products
        self.schedule = schedule

class ZipMarkets(object):
    
    def __init__(self, identity, zipcode, market_id, marketname):
        self.identity = identity
        self.zipcode = zipcode
        self.market_id = market_id
        self.marketname = marketname
