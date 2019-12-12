import urllib

from flask import request, json


def get_midrate(fromCurrency):
        url = "https://api.exchangeratesapi.io/latest?base="
        json_data = getResponse(url + fromCurrency)
        return json_data['rates']


def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if operUrl.getcode() == 200:
        data1 = operUrl.read()
        jsonData = json.loads(data1)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData
