import psycopg2
import json

import margin_calculator
import midrate
import pandas as pd

from sqlalchemy import create_engine

table_name = "margintest"


class Postgres:
    def __init__(self):
        self.con = psycopg2.connect(database="postgres",
                                    user="postgres",
                                    password="postgres",
                                    host="127.0.0.1",
                                    port="5432")

        print("Database opened successfully init")

    def createTable(self):
        try:
            print("Database opened successfully create")
            cur = self.con.cursor()
            cur.execute('''CREATE TABLE margintest
                  (NameBank text NOT NULL,
                 Country text NOT NULL,
                 TimeStamp time not null,
                 Fcurrency text not null,
                 Tcurrency text not null,
                 Mbuy numeric not null,
                 Msell numeric not null, 
                 Pbuy numeric not null,
                 Psell numeric not null,
                 BuyExchange numeric not null,
                 SellExchange numeric not null,
                 MidRate numeric not null,
                 CONSTRAINT margin_pk PRIMARY KEY (NameBank, Country, TimeStamp)

                 )''')
            print("Table created successfully")

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()

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

            engine = create_engine('postgresql://postgres:postgres@135.228.162.15: 5432/postgres')
            df1.to_sql("margintest_df_calc", engine, if_exists='append', index=False)

            print("Bank inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print(error)

    def insert_data(self, data):
        try:
            print("Database opened successfully insert")

            cur = self.con.cursor()
            insert_query = ('''INSERT INTO margintest(namebank, country, timestamp, fcurrency, 
                                                        tcurrency, mbuy, msell, pbuy, psell,
                                                        buyExchange, sellExchange, midrate) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''')

            if data.unit == 'M100':
                value_to_insert = (data.name, data.country, data.time,
                                   data.fromCurrency, data.toCurrency,
                                   data.buyMargin, data.sellMargin,
                                   margin_calculator.margin_to_percentage(data), margin_calculator.margin_to_percentage(data),
                                   margin_calculator.margin_to_exchange_rate(data), margin_calculator.margin_to_exchange_rate(data),
                                   midrate.get_midrate(data))

            elif data.unit == 'exchange':
                value_to_insert = (data.name, data.country, data.time,
                                   data.fromCurrency, data.toCurrency,
                                   margin_calculator.exchange_rate_to_margin(data), margin_calculator.exchange_rate_to_margin(data),
                                   margin_calculator.exchange_rate_to_percentage(data), margin_calculator.exchange_rate_to_percentage(data),
                                   data.buyMargin, data.sellMargin,
                                   midrate.get_midrate(data))

            elif data.unit == 'percentage':
                value_to_insert = (data.name, data.country, data.time,
                                   data.fromCurrency, data.toCurrency,
                                   margin_calculator.percentage_to_margin(data), margin_calculator.percentage_to_margin(data),
                                   data.buyMargin, data.sellMargin,
                                   margin_calculator.percentage_to_exchange_rate(data), margin_calculator.percentage_to_exchange_rate(data),
                                   midrate.get_midrate(data))

            print(value_to_insert)

            cur.execute(insert_query, value_to_insert)

            print("Bank inserted successfully")
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()

    def truncate(self):
        try:
            print("Database opened successfully truncate")
            cur = self.con.cursor()
            cur.execute('''TRUNCATE TABLE margintest RESTART IDENTITY;''')
            print("db truncated")
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()

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
