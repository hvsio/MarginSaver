from flask import Flask, request, jsonify
from margins import Margin
from sql_connection import Postgres


app = Flask(__name__)


@app.route("/margin", methods=['POST'])
def getData():
    if request.method == 'POST':
        try:
            posted_data = request.get_json()
            print(posted_data)

            create_object_margin = Margin(**posted_data)

            conn_ref = Postgres()
            conn_ref.insert_data(create_object_margin)
            return jsonify({"status": "added"}), 201
        except:
            jsonify({"status": "Postgres error"}), 408


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
