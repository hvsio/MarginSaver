import json
from bson import ObjectId



class Margin:
    def __init__(self, bank, time, *args, **kwargs):
        self.id = ObjectId()
        self.bank = bank
        self.time = time

    def __getTime__(self):
        return self.time

    def __getBankID__(self):
        return self.id

    def __getBank__(self):
        return self.bank

    def to_JSON(self):
        string = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(string)
