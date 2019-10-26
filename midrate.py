import urllib

from flask import request, json


def getMidrate(fromCur, toCur):
    url = "https://api.exchangeratesapi.io/latest?base="
    json_data = getResponse(url + toCur)
    return json_data['rates'][fromCur]



def getMidrateFromToCur(data):
    url = "https://api.exchangeratesapi.io/latest?base="
    json_data = getResponse(url + data.fromCurrency)
    for item in json_data['rates']:
        if item == data.toCurrency:
            return json_data['rates'][item]


def getResponse(url):
    operUrl = urllib.request.urlopen(url)
    if (operUrl.getcode() == 200):
        data1 = operUrl.read()
        jsonData = json.loads(data1)
    else:
        print("Error receiving data", operUrl.getcode())
    return jsonData
