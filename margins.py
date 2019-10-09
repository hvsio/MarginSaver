import json
from bson import ObjectId


class Margin:
    def __init__(self, name, country, time, fromCurrency, toCurrency, buyValue, sellValue, unit, *args, **kwargs):
        self.id = ObjectId()
        self.name = name
        self.country = country
        self.time = time
        self.fromCurrency = fromCurrency
        self.toCurrency = toCurrency
        self.buyValue = buyValue
        self.sellValue = sellValue
        self.unit = unit

    def __getTime__(self):
        return self.time

    def __getBankID__(self):
        return self.id

    def __getBank__(self):
        return self.bank

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)
