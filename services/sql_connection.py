import sys
import psycopg2
import json
from services import margin_calculator
import pandas as pd
from sqlalchemy import *
import threading
from environment.environment import Config

table_name = "margin"


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
                    "date": data.time,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": margin_calculator.invert_margin(data) if data.isCrossInverted else data.buyMargin,
                    "sellmargin": margin_calculator.invert_margin(data) if data.isCrossInverted else data.sellMargin,
                    "exchangeratesell": margin_calculator.margin_to_exchange_rate_sell(data),
                    "exchangeratebuy": margin_calculator.margin_to_exchange_rate_buy(data),
                    "percentbuy": margin_calculator.margin_to_percentage(data),
                    "percentsell": margin_calculator.margin_to_percentage(data),
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "percentage":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "date": data.time,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": margin_calculator.percentage_to_margin(data),
                    "sellmargin": margin_calculator.percentage_to_margin(data),
                    "exchangeratesell": margin_calculator.percentage_to_exchange_rate_sell(data),
                    "exchangeratebuy": margin_calculator.percentage_to_exchange_rate_buy(data),
                    "percentbuy": data.buyMargin,
                    "percentsell": data.sellMargin,
                    "unit": data.unit,
                    "midrate": margin_calculator.get_midrate_from_panda(data),
                }
            elif data.unit == "exchange":
                df = {
                    "name": data.name,
                    "country": data.country,
                    "date": data.time,
                    "time": data.time,
                    "tocurrency": data.toCurrency,
                    "fromcurrency": data.fromCurrency,
                    "buymargin": margin_calculator.exchange_rate_to_margin(data),
                    "sellmargin": margin_calculator.exchange_rate_to_margin(data),
                    "exchangeratesell":
                        margin_calculator.exchange_inverted_calculate(data.buyMargin, data.isCrossInverted)
                    if data.isCrossInverted else
                        margin_calculator.exchange_inverted_calculate(data.sellMargin, data.isCrossInverted),
                    "exchangeratebuy":
                        margin_calculator.exchange_inverted_calculate(data.sellMargin, data.isCrossInverted)
                    if data.isCrossInverted else
                        margin_calculator.exchange_inverted_calculate(data.buyMargin, data.isCrossInverted),
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

            df1.to_sql(table_name, engine, if_exists='append', index=False)

            print("Bank inserted successfully")

            print("Creating inverted entry")

            df_inverted = margin_calculator.invert_dataframe(df1)
            df_inverted.to_sql(table_name, engine, if_exists='append', index=False)

            print("Inverted entry inserted successfully")


    def get_last_exchange_buy_from_banks(self, country, fromCurrency, toCurrency):
        # exchangeratebuy from customer perspective for example:
         # fromCurrency: DKK
         # toCurrency: EUR
         # Danske bank buy DKK EUR at a rate of 0.1336
        try:
            print("Database opened successfully get calc")
            cursor = self.con.cursor()
            query = "SELECT DISTINCT ON (name, country, tocurrency, fromcurrency) " \
                    "date + time as MostRecentDate, name, country, tocurrency, fromcurrency, exchangeratesell as exchangeratebuy " \
                    "FROM margin " \
                    "WHERE country = (%s) AND fromcurrency = (%s) AND tocurrency = (%s) " \
                    "ORDER BY name, country, tocurrency, fromcurrency, exchangeratesell, date DESC, time DESC; "
            cursor.execute(query, (country, fromCurrency, toCurrency))
            data = cursor.fetchall()
            cols = list(map(lambda x: x[0], cursor.description))
            response = pd.DataFrame(data, columns=cols).to_json(orient='records', date_format='iso')
            return json.loads(response)

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            self.con.commit()
            self.con.close()

    def table_exists(self, table_str):
        exists = False
        try:
            cur = self.con.cursor()
            cur.execute("select exists(select relname from pg_class where relname='" + table_str + "')")
            exists = cur.fetchone()[0]
            cur.close()
        except psycopg2.Error as e:
            print(str(e))
        return exists

    def initialize_DB(self):
        cur = self.con.cursor()
        try:
            if not self.table_exists(table_name):
                cur.execute("""CREATE TABLE margin(    
                                    id SERIAL,  
                                    name TEXT, 
                                    country TEXT, 
                                    date DATE,
                                    time TIME, 
                                    tocurrency TEXT, 
                                    fromcurrency TEXT, 
                                    buymargin REAL, 
                                    sellmargin REAL, 
                                    exchangeratesell REAL, 
                                    exchangeratebuy REAL, 
                                    percentbuy REAL, 
                                    percentsell REAL, 
                                    unit TEXT, 
                                    midrate REAL, 
                                    PRIMARY KEY (id))""")
                self.con.commit()
        except Exception as e:
            print(str(e))
        finally:
            self.con.commit()
            self.con.close()
