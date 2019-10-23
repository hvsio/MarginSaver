import midrate


def marToEx(data):
    mid = midrate.getMidrateFromToCur(data)
    bankMSell = float(data.sellMargin)
    return mid + bankMSell


def marToP(data):
    mid = midrate.getMidrateFromToCur(data)
    bankMSell = float(data.sellMargin)
    return (bankMSell / mid) * 100


def exToM(data):
    mid = midrate.getMidrateFromToCur(data)
    bankExSell = float(data.sellMargin)
    return bankExSell - mid


def exToP(data):
    mid = midrate.getMidrateFromToCur(data)
    bankExSell = float(data.sellMargin)
    return ((bankExSell - mid) / mid) * 100


def pToEx(data):
    mid = midrate.getMidrateFromToCur(data)
    bankPSell = float(data.sellMargin)
    return ((bankPSell * mid) / 100) + mid


def pToM(data):
    mid = midrate.getMidrateFromToCur(data)
    bankPSell = float(data.sellMargin)
    return (bankPSell * mid) / 100
