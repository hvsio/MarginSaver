import psycopg2
from psycopg2._json import Json
import bson.tz_util
import dump
import json
import sqlalchemy

table_name = "margintest2"

class Postgres:
    def __init__(self):
        con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")

        print("Database opened successfully init")

    def createTable(self):
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")

            print("Database opened successfully create")
            cur = con.cursor()
            cur.execute('''CREATE TABLE margintest2
                  (ID time PRIMARY KEY  NOT NULL,
                 INFO VARCHAR NOT NULL)''')
            print("Table created successfully")

            con.commit()
            con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)

    def insert_data(self, data):
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")

            print("Database opened successfully insert")

            cur = con.cursor()
            insert_query = ('''INSERT INTO margintest2(ID, INFO)  VALUES (%s,%s)''')

            value_to_insert = (data.__getTime__(), data.__getBank__())
            print(value_to_insert)


            cur.execute(insert_query, value_to_insert)

            print("Bank inserted successfully")
            con.commit()
            con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)



    def insert_bank(self, margin):
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")

            print("Database opened successfully insert")

            cur = con.cursor()


            value_to_insert = margin.to_JSON()
            print(value_to_insert)
            insert_query_json =('''
                select * from json_to_record() as x(id numeric , bank text ,time numeric )''')

            cur.execute(insert_query_json)
            print("Bank inserted successfully")
            con.commit()
            con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)


    def insert_json_object(self, data):

        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1", port="5432")

            print("Database opened successfully insert json")

            cur = con.cursor()
            cur.execute("Truncate {} Cascade;".format(table_name))
            print("Truncated {}".format(table_name))
            bank = data.to_JSON()
            print(data)
            print(bank)
            for record in bank:
                record = dump(record)
                cur.execute(("INSERT INTO {} VALUES ('{}')".format(table_name, str(record).replace("'", "<>"))))
                cur.execute("commit;")

            print("Inserted data into {}".format(table_name))
            con.close()
            print("DB connection closed.")

        except Exception as e:
            print('Error {}'.format(str(e)))

    def truncate(self):
        try:
            con = psycopg2.connect(database="postgres", user="postgres", password="postgres", host="127.0.0.1",
                                   port="5432")

            print("Database opened successfully truncate")
            cur = con.cursor()
            cur.execute('''TRUNCATE TABLE margintest2 RESTART IDENTITY;''')
            print("db truncated")
            con.commit()
            con.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
