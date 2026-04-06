from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Fetch real congressional trading data from official APIs
CONGRESS_API_URL = 'https://api.congress.gov/v3/trading'

@app.route('/trades', methods=['GET'])
def get_trades():
    # Example function to fetch trades
    response = requests.get(CONGRESS_API_URL + '/trades')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Unable to fetch trades'}), response.status_code

@app.route('/politician/<id>', methods=['GET'])
def get_politician_profile(id):
    # Example function to fetch politician profile
    response = requests.get(CONGRESS_API_URL + f'/politicians/{id}')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Politician not found'}), 404

@app.route('/sector_analysis', methods=['GET'])
def get_sector_analysis():
    # Example function to fetch sector analysis
    response = requests.get(CONGRESS_API_URL + '/sector_analysis')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Unable to fetch sector analysis'}), response.status_code

@app.route('/alerts', methods=['GET'])
def get_alerts():
    # Example function to fetch alerts
    response = requests.get(CONGRESS_API_URL + '/alerts')
    if response.status_code == 200:
        return jsonify(response.json()), 200
    return jsonify({'error': 'Unable to fetch alerts'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)