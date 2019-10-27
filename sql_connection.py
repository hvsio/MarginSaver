import psycopg2
import json

import margin_calculator
import midrate
import pandas as pd

from sqlalchemy import create_engine

table_name = "margintest"


class Postgres:

    def insert_with_panda(self, data):

        #FIXME: find better(readable) way to distribute depending on unit
        try:
            print("Database opened successfully panda")
            if data.unit == "M100":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "toCurrency": data.toCurrency,
                    "fromCurrency": data.fromCurrency,
                    "buyMargin": data.buyMargin,
                    "sellMargin": data.sellMargin,
                    "exchangeRateSell": margin_calculator.margin_to_exchange_rate(data),
                    "exchangeRateBuy": margin_calculator.margin_to_exchange_rate(data),
                    "percentBuy": margin_calculator.margin_to_percentage(data),
                    "percentSell": margin_calculator.margin_to_percentage(data),
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "Percent":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "toCurrency": data.toCurrency,
                    "fromCurrency": data.fromCurrency,
                    "buyMargin": margin_calculator.percentage_to_margin(data),
                    "sellMargin": margin_calculator.percentage_to_margin(data),
                    "exchangeRateSell": margin_calculator.percentage_to_exchange_rate(data),
                    "exchangeRateBuy": margin_calculator.percentage_to_exchange_rate(data),
                    "percentBuy": data.buyMargin,
                    "percentSell": data.sellMargin,
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "Exchange":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "toCurrency": data.toCurrency,
                    "fromCurrency": data.fromCurrency,
                    "buyMargin": margin_calculator.exchange_rate_to_margin(data),
                    "sellMargin": margin_calculator.exchange_rate_to_margin(data),
                    "exchangeRateSell": data.sellMargin,
                    "exchangeRateBuy": data.buyMargin,
                    "percentBuy": margin_calculator.exchange_rate_to_percentage(data),
                    "percentSell": margin_calculator.exchange_rate_to_percentage(data),
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }

            df1 = pd.DataFrame(df)

            engine = create_engine('postgresql://postgres:holadontsteal@135.228.162.15:5432/postgres')
            df1.to_sql("margintest_df_calc", engine, if_exists='append', index=False)

            print("Bank inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print(error)


    def get_all_data(self):
        try:
            print("Database opened successfully get")
            cur = self.con.cursor()
            cur.execute('''SELECT * FROM margintest;''')
            data = cur.fetchall()
            for row in data:
                print(row)
            return json.dumps(data, indent=4, sort_keys=True, default=str)

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()
