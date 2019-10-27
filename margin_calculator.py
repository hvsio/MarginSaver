import midrate

def margin_to_exchange_rate(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankMSell = float(j['sellMargin'][idx])
            list_p.append(mid + bankMSell)
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p


def margin_to_percentage(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankMSell = float(j['sellMargin'][idx])
            list_p.append(((bankMSell / mid*100)))
        except Exception as e:
            list_p.append(0)
            print(str(e))
    print(list_p)
    return list_p


def exchange_rate_to_margin(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankExSell = float(j['sellMargin'][idx])
            list_p.append(bankExSell - mid)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def exchange_rate_to_percentage(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankExSell = float(j['sellMargin'][idx])
            list_p.append(((bankExSell - mid) / mid*100))
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def percentage_to_exchange_rate(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankPSell = float(j['sellMargin'][idx])
            list_p.append(((bankPSell * mid) / 100) + mid)
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p


def percentage_to_margin(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            bankPSell = float(j['sellMargin'][idx])
            list_p.append((bankPSell * mid) / 100)
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p

def get_midrate_from_panda(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid = midrate.get_midrate_from_to(j['fromCurrency'][idx], j['toCurrency'][idx])
            list_p.append(mid)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p
