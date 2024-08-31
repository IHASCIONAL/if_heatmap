from flask import Flask, jsonify
from backend import DataFetcher

app = Flask(__name__)
data_fetcher = DataFetcher()

@app.route('/logistic-regions', methods=['GET'])
def get_logistic_regions():
    try:
        regions = data_fetcher.fetch_logistic_regions()
        return jsonify(regions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Configure a porta e o IP de escuta conforme necessário
