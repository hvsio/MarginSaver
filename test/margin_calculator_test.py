import unittest
import margin_calculator
from scrapped_data import Scrapped


class MyTestCase(unittest.TestCase):
    @unittest.skip("this calculation breaks, mid-rate uses a API that changes value every day.")
    def test_percentage_to_exchange_rate_correct(self):
        data = correct_scrapped_data()
        result = margin_calculator.percentage_to_exchange_rate_buy(data)
        expected_result = [7.566021119999999, 6.8119394256192, 8.799057714929999, 0.69722342782896, 0.73541619989548,
                           6.847358199437, 5.204723589038999, 0.0619549468752, 5.0748391016741, 0.8637714364751999,
                           4.6502895635832, 4.3339104491660905, 1.7655689739717, 0.29257216212497, 0.02271990177174,
                           1.1979575080150502, 0.22341633238320002, 0.463487101792, 0.1056893256378]
        self.assertEqual(result, expected_result)



# TODO: write unit tests for all calculation methods


def correct_scrapped_data():
    input = {
        "name": "FynskeBank",
        "country": "DK",
        "time": "21-Oct-2019 (09:58:01.694763)",
        "toCurrency": ["EUR", "USD", "GBP", "SEK", "NOK", "CHF", "CAD", "JPY", "SGD", "HKD", "AUD", "NZD", "PLN", "CZK",
                       "HUF", "TRY", "THB", "ZAR", "RUB"],
        "fromCurrency": ["DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK", "DKK",
                         "DKK", "DKK", "DKK", "DKK", "DKK", "DKK"],
        "buyMargin": ["1.2800", "1.2800", "2.0000", "0.2800", "0.2800", "1.0000", "1.1000", "0.0100", "2.8500",
                      "0.6500", "1.2800", "1.2700", "1.1000", "0.1350", "0.0200", "2.6500", "0.2000", "0.7500",
                      "0.2000"],
        "sellMargin": ["1.2800", "1.2800", "2.0000", "0.2800", "0.2800", "1.0000", "1.1000", "0.0100", "2.8500",
                       "0.6500", "1.2800", "1.2700", "1.1000", "0.1350", "0.0200", "2.6500", "0.2000", "0.7500",
                       "0.2000"],
        "unit": "Percent"
    }

    return Scrapped(**input)
