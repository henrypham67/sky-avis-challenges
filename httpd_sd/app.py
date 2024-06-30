from flask import Flask, jsonify
import requests
from prometheus_client import Gauge, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST
from prometheus_client.core import GaugeMetricFamily

app = Flask(__name__)

# Replace with your Infura Project ID
API_KEY = 'f1419cc2c9fe47649d318bb0d689d01b'
ANKR_URL = 'https://rpc.ankr.com/eth'
INFURA_URL = f'https://mainnet.infura.io/v3/{API_KEY}'

HEADERS = {
    "Content-Type": "application/json"
}

# Create Prometheus metrics
registry = CollectorRegistry()
block_difference_metric = Gauge('block_difference', 'Difference in block numbers between Ankr and Infura', registry=registry)
ankr_block_metric = Gauge('ankr_block_number', 'Current block number from Ankr', registry=registry)
infura_block_metric = Gauge('infura_block_number', 'Current block number from Infura', registry=registry)


def get_block_number(url):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    response = requests.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    result = response.json()
    return int(result["result"], 16)


@app.route('/probe', methods=['GET'])
def check_block_difference():
    try:
        infura_block_number = get_block_number(INFURA_URL)
        ankr_block_number = get_block_number(ANKR_URL)

        difference = ankr_block_number - infura_block_number

        # Update Prometheus metrics
        block_difference_metric.set(difference)
        ankr_block_metric.set(ankr_block_number)
        infura_block_metric.set(infura_block_number)

        return jsonify({
            "infura_block_number": infura_block_number,
            "ankr_block_number": ankr_block_number,
            "difference": "success" if difference < 5 else "fail"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
