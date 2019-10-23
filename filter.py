import midrate

def distribute(data):
    if data.unit == "M100":
        data.buyMargin



def marToEx(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankMSell = float(j['sellMargin'][idx])
        list_p.append(mid + bankMSell)

    return list_p


def marToP(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankMSell = float(j['sellMargin'][idx])
        list_p.append(((bankMSell / mid) * 100))

    print(list_p)
    return list_p


def exToM(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankExSell = float(j['sellMargin'][idx])
        list_p.append(bankExSell - mid)

    return list_p


def exToP(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankExSell = float(j['sellMargin'][idx])
        list_p.append(((bankExSell - mid) / mid) * 100)

    return list_p


def pToEx(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankPSell = float(j['sellMargin'][idx])
        list_p.append(((bankPSell * mid) / 100) + mid)

    return list_p


def pToM(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        mid = midrate.getMidrate(j['fromCurrency'][idx], j['toCurrency'][idx])
        bankPSell = float(j['sellMargin'][idx])
        list_p.append((bankPSell * mid) / 100)

    return list_p
