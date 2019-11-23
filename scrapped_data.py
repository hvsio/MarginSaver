import json
from bson import ObjectId


class Scrapped:
    def __init__(self, name, country, time, fromCurrency, toCurrency, isCrossInverted, buyMargin, sellMargin, unit,
                 *args, **kwargs):
        self.id = ObjectId()
        self.name = name
        self.country = country
        self.time = time
        self.fromCurrency = fromCurrency
        self.toCurrency = toCurrency
        self.isCrossInverted = isCrossInverted
        self.buyMargin = [float(i) for i in buyMargin]
        self.sellMargin = [float(i) for i in sellMargin]
        self.unit = unit

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)

    def base_margin(self):
        if self.unit == 'M100':
            self.buyMargin = [float(element) / 100 for element in self.buyMargin]
            self.sellMargin = [float(element) / 100 for element in self.sellMargin]
