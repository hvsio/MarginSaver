from flask import Flask, request, jsonify, json, Response
from models.scrapped_data import Scrapped
from services.sql_connection import Postgres

app = Flask(__name__)

conn_ref = Postgres()
conn_ref.initialize_DB()


@app.route("/margin", methods=['POST'])
def postData():
    try:
        posted_data = request.get_json()
        print(posted_data)
        create_object_margin = Scrapped(**posted_data)
        create_object_margin.base_margin()
        conn_ref = Postgres()
        conn_ref.insert_with_panda(create_object_margin)
        return jsonify({"status": "added"}), 201
    except Exception as e:
        print(str(e))
        return jsonify({"status": "Postgres error"}), 408


@app.route("/margin", methods=['GET'])
def get_data():
    try:
        conn_ref = Postgres()
        return conn_ref.get_all_data()

    except:
        return jsonify({"status": "Postgres error"}), 408


@app.route("/banksbuyrate", methods=['GET'])
def get_banks_latest_exchange_buy():
    try:
        country = request.values.get('country')
        fromCurrency = request.values.get('fromCurrency')
        toCurrency = request.values.get('toCurrency')
        conn_ref = Postgres()
        response = conn_ref.get_last_exchange_buy_from_banks(country, fromCurrency, toCurrency)
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')
    except Exception as e:
        print(str(e))
        return jsonify({"status": "Postgres error"}), 408


@app.route("/initializedb", methods=["GET"])
def init_db():
    try:
        conn_ref = Postgres()
        conn_ref.initialize_DB()
        return jsonify({"status": "DB initialize"}), 200

    except Exception as E:
        print(str(E))
        return jsonify({"status": "postgres serror"}), 408


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
