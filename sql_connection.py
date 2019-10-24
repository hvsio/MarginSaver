import psycopg2
from psycopg2._json import Json
import bson.tz_util
import dump
import json

import df_util
import filter
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
        try:
            print("Database opened successfully panda")


            df = {
                "name": data.name,
                "country": data.country,
                "time": data.time,
                "toCurrency": data.toCurrency,
                "fromCurrency":  data.fromCurrency,
                "buyMargin": data.buyMargin,
                "sellMargin": data.sellMargin,
                "percentBuy": filter.marToP(data),
                "percentSell": filter.marToP(data),
                "exchangeRateSell": filter.marToEx(data),
                "exchangeRateBuy": filter.marToEx(data),
                "unit": data.unit
            }


            df1 = pd.DataFrame(df)
            engine = create_engine('postgresql://postgres:postgres@127.0.0.1: 5432/postgres')
            df1.to_sql("margintest3", engine, if_exists='append', index=False)

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
                                   filter.marToP(data), filter.marToP(data),
                                   filter.marToEx(data), filter.marToEx(data),
                                   midrate.getMidrateFromToCur(data))

            elif data.unit == 'Exchange':
                value_to_insert = (data.name, data.country, data.time,
                                   data.fromCurrency, data.toCurrency,
                                   filter.exToM(data), filter.exToM(data),
                                   filter.exToP(data), filter.exToP(data),
                                   data.buyMargin, data.sellMargin,
                                   midrate.getMidrateFromToCur(data))

            elif data.unit == 'Percentage':
                value_to_insert = (data.name, data.country, data.time,
                                   data.fromCurrency, data.toCurrency,
                                   filter.pToM(data), filter.pToM(data),
                                   data.buyMargin, data.sellMargin,
                                   filter.pToEx(data), filter.pToEx(data),
                                   midrate.getMidrateFromToCur(data))

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
