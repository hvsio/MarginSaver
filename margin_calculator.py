import midrate


def margin_to_exchange_rate_sell(data):
    if data.isCrossInverted:
        return calculate(data, lambda midrate_value, bank_value: 1 / (midrate_value + bank_value))
    return calculate(data, lambda midrate_value, bank_value: midrate_value + bank_value)


def margin_to_exchange_rate_buy(data):
    if data.isCrossInverted:
        return calculate(data, lambda midrate_value, bank_value: 1 / (midrate_value - bank_value))
    return calculate(data, lambda midrate_value, bank_value: midrate_value - bank_value)


def margin_to_percentage(data):
    return calculate(data, lambda midrate_value, bank_value: (bank_value / midrate_value) * 100)


def percentage_to_exchange_rate_sell(data):
    if data.isCrossInverted:
        return calculate(data,
                         lambda midrate_value, bank_value: 1 / (midrate_value + ((bank_value * midrate_value) / 100)))

    return calculate(data, lambda midrate_value, bank_value: midrate_value + ((bank_value * midrate_value) / 100))


def percentage_to_exchange_rate_buy(data):
    if data.isCrossInverted:
        return calculate(data,
                         lambda midrate_value, bank_value: 1 / (midrate_value - ((bank_value * midrate_value) / 100)))
    return calculate(data, lambda midrate_value, bank_value: midrate_value - ((bank_value * midrate_value) / 100))


def percentage_to_margin(data):
    return calculate(data, lambda midrate_value, bank_value: (bank_value * midrate_value) / 100)



def calculate(data, operation):
    j = data.to_JSON()
    list_p = []
    mid = midrate.Midrate.get_midrate(j["fromCurrency"][0])
    for idx, val in enumerate(j['toCurrency']):
        try:
            if data.isCrossInverted:
                mid_current = 1 / get_key(mid, j['toCurrency'][idx])
            else:
                mid_current = get_key(mid, j['toCurrency'][idx])

            bankMSell = float(j['sellMargin'][idx])
            list_p.append(operation(mid_current, bankMSell))
        except Exception as e:
            list_p.append(0)
            print(str(e))

    return list_p


def exchange_rate_to_margin(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            bankExSell = float(j['sellMargin'][idx])
            bankExBuy = float(j['buyMargin'][idx])
            if data.isCrossInverted:
                list_p.append(1 / ((bankExBuy - bankExSell) / 2))
            else:
                list_p.append((bankExBuy - bankExSell) / 2)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def exchange_rate_to_percentage(data):
    j = data.to_JSON()
    list_p = []
    for idx, val in enumerate(j['toCurrency']):
        try:
            bankExBuy = float(j['buyMargin'][idx])
            bankExSell = float(j['sellMargin'][idx])
            mid_current = (bankExBuy + bankExSell) / 2
            margin = bankExBuy - mid_current
            if data.isCrossInverted:
                list_p.append(1 / ((margin / mid_current) * 100))
            else:
                list_p.append((margin / mid_current) * 100)
        except Exception as e:
            list_p.append(0)
            print(str(e))
    return list_p


def exchange_inverted_calculate(input_list, is_inverted):
    if is_inverted:
        return [1 / x for x in input_list]
    else:
        return input_list


def get_midrate_from_panda(data):
    j = data.to_JSON()
    list_p = []
    mid = midrate.Midrate.get_midrate(j["fromCurrency"][0])
    # returns (json) dict with base and all rates, API is called only once
    for idx, val in enumerate(j['toCurrency']):
        try:
            if data.isCrossInverted:
                mid_current = 1 / get_key(mid, j['toCurrency'][idx])
            else:
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
