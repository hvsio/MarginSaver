import json
from bson import ObjectId


class Scrapped:
    def __init__(self, name, country, time, fromCurrency, toCurrency, buyMargin, sellMargin, unit, *args, **kwargs):
        self.id = ObjectId()
        self.name = name
        self.country = country
        self.time = time
        self.fromCurrency = fromCurrency
        self.toCurrency = toCurrency
        self.buyMargin = buyMargin
        self.sellMargin = sellMargin
        self.unit = unit

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)
