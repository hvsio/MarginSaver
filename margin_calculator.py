import midrate



def margin_to_exchange_rate(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankMSell = float(j['sellMargin'][idx])
            list_p.append(mid_current + bankMSell)
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p


def margin_to_percentage(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankMSell = float(j['sellMargin'][idx])
            list_p.append((bankMSell / mid_current * 100))
        except Exception as e:
            list_p.append(0)
            print(str(e))
    print(list_p)
    return list_p


def exchange_rate_to_margin(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankExSell = float(j['sellMargin'][idx])
            list_p.append(bankExSell - mid_current)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def exchange_rate_to_percentage(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankExSell = float(j['sellMargin'][idx])
            list_p.append(((bankExSell - mid_current) / mid_current * 100))
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def percentage_to_exchange_rate(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankPSell = float(j['sellMargin'][idx])
            list_p.append(((bankPSell * mid_current) / 100) + mid_current)
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p


def percentage_to_margin(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            bankPSell = float(j['sellMargin'][idx])
            list_p.append((bankPSell * mid_current) / 100)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def get_midrate_from_panda(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.get_midrate(j["fromCurrency"][0])
    # returns (json) dict with base and all rates, API is called only once
    for idx, val in enumerate(j['toCurrency']):
        try:
            mid_current = get_key(mid, j['toCurrency'][idx])
            list_p.append(mid_current)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def get_key(dict, key):
    if key in dict.keys():
        return dict[key]
    else:
        raise KeyError('Key not found')
