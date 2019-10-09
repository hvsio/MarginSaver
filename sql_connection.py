import psycopg2
from psycopg2._json import Json
import bson.tz_util
import dump
import json
import sqlalchemy

table_name = "margintest2"


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
                 Mbuy money not null,
                 Msell money not null, 
                 Pbuy money not null,
                 Psell money not null,
                 BuyExchange money not null,
                 SellExchange money not null,
                 MidRate money not null,
                 CONSTRAINT margin_pk PRIMARY KEY (NameBank, Country, TimeStamp)

                 )''')
            print("Table created successfully")

            self.con.commit()
            self.con.close()
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

            value_to_insert = (data.name, data.country, data.time, data.fromCurrency,
                               data.toCurrency, data.buyValue, data.sellValue, 1, 2, 3, 4, 5)

            print(value_to_insert)

            cur.execute(insert_query, value_to_insert)

            print("Bank inserted successfully")
            self.con.commit()
            self.con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)

    def truncate(self):
        try:
            print("Database opened successfully truncate")
            cur = self.con.cursor()
            cur.execute('''TRUNCATE TABLE margintest RESTART IDENTITY;''')
            print("db truncated")
            self.con.commit()
            self.con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
