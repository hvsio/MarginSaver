from flask import Flask, request, jsonify, json
from margins import Margin
from sql_connection import Postgres

app = Flask(__name__)


@app.route("/margin", methods=['POST'])
def postData():
    try:
        posted_data = request.get_json()
        print(posted_data)
        create_object_margin = Margin(**posted_data)
        conn_ref = Postgres()
        conn_ref.insert_with_panda(create_object_margin)
        return jsonify({"status": "added"}), 201
    except Exception as e:
        print(str(e))
        jsonify({"status": "Postgres error"}), 408


@app.route("/margin", methods=['GET'])
def getData():
    try:
        conn_ref = Postgres()
        return conn_ref.get_all_data()

    except:
        jsonify({"status": "Postgres error"}), 408


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
