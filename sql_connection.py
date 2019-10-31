import sys
import psycopg2
import json
import sqlalchemy
import margin_calculator
import midrate
import pandas as pd
from sqlalchemy import *
import threading
from environment.environment import Config

table_name = "margintest"



class Postgres:
    def __init__(self):

        self.lock = threading.Lock()
        Config.initialize()
        self.environment = Config.cloud('DATABASE') if (len(sys.argv) > 1 and sys.argv[1] == 'cloud') \
            else Config.dev('DATABASE')

        self.con = psycopg2.connect(self.environment)

        print("Database opened successfully init")

    def insert_with_panda(self, data):
        with self.lock:
            # FIXME: find better(readable) way to distribute depending on unit

            print("Database opened successfully panda")
            if data.unit == "M100":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": data.buyMargin,
                    "sellmargin": data.sellMargin,
                    "exchangeratesell": margin_calculator.margin_to_exchange_rate(data),
                    "exchangeratebuy": margin_calculator.margin_to_exchange_rate(data),
                    "percentbuy": margin_calculator.margin_to_percentage(data),
                    "percentsell": margin_calculator.margin_to_percentage(data),
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "percentage":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": margin_calculator.percentage_to_margin(data),
                    "sellmargin": margin_calculator.percentage_to_margin(data),
                    "exchangeratesell": margin_calculator.percentage_to_exchange_rate(data),
                    "exchangeratebuy": margin_calculator.percentage_to_exchange_rate(data),
                    "percentbuy": data.buyMargin,
                    "percentsell": data.sellMargin,
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "exchange":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": margin_calculator.exchange_rate_to_margin(data),
                    "sellmargin": margin_calculator.exchange_rate_to_margin(data),
                    "exchangeratesell": data.sellMargin,
                    "exchangeratebuy": data.buyMargin,
                    "percentbuy": margin_calculator.exchange_rate_to_percentage(data),
                    "percentsell": margin_calculator.exchange_rate_to_percentage(data),
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }

            df1 = pd.DataFrame(df)

            df1['buymargin'] = pd.to_numeric(df['buymargin'])
            df1['sellmargin'] = pd.to_numeric(df['sellmargin'])
            df1['exchangeratesell'] = pd.to_numeric(df['exchangeratesell'])
            df1['exchangeratebuy'] = pd.to_numeric(df['exchangeratebuy'])
            df1['percentbuy'] = pd.to_numeric(df['percentbuy'])
            df1['percentsell'] = pd.to_numeric(df['percentsell'])

            print(df1)

            engine = create_engine(self.environment)

            df1.to_sql("margintest", engine, if_exists='append', index=False)

            print("Bank inserted successfully")



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

    def get_all_of_to_currency(self, tocurrency):
        try:
            print("Database opened successfully get")
            cur = self.con.cursor()
            query_to_execute = "SELECT * FROM margintest WHERE margintest.tocurrency IN (%s)"
            cur.execute(query_to_execute, (tocurrency,))
            data = cur.fetchall()
            for row in data:
                print(row)
            return json.dumps(data, indent=4, sort_keys=True, default=str)

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()