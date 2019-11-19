from flask import Flask, request, jsonify, json, Response
from scrapped_data import Scrapped
from sql_connection import Postgres

app = Flask(__name__)


@app.route("/margin", methods=['POST'])
def postData():
    try:
        posted_data = request.get_json()
        print(posted_data)
        create_object_margin = Scrapped(**posted_data)
        if create_object_margin.unit == 'M100': create_object_margin.base_margin()
        conn_ref = Postgres()
        conn_ref.insert_with_panda(create_object_margin)
        return jsonify({"status": "added"}), 201
    except Exception as e:
        print(str(e))
        return jsonify({"status": "Postgres error"}), 408


@app.route("/margin", methods=['GET'])
def getData():
    try:
        conn_ref = Postgres()
        return conn_ref.get_all_data()

    except:
        return jsonify({"status": "Postgres error"}), 408


@app.route("/banksbuyrate", methods=['GET'])
def get_banks_latest_exchange_buy():
    try:
        conn_ref = Postgres()
        country = request.values.get('country')
        fromCur = request.values.get('fromCur')
        toCur = request.values.get('toCur')
        response = conn_ref.get_last_exchange_buy_from_banks(country, fromCur, toCur)
        '''response = json.dumps()
        response = json.loads(response)'''
        print(type(response))
        return Response(response=json.dumps(response),
                        status=200,
                        mimetype='application/json')
    except Exception as e:
        print(str(e))
        return jsonify({"status": "Postgres error"}), 408


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
