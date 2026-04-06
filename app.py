"""
Alpha Tracker Pro - Real-time Congressional Trading Dashboard
Backend server for fetching live government disclosure data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import sqlite3
from threading import Thread

app = Flask(__name__)
CORS(app)

class CongressionalDataFetcher:
    """Fetches real-time data from official government APIs"""
    
    def __init__(self):
        self.house_url = "https://disclosures-clerk.house.gov/api/FinancialDisclosure"
        self.senate_url = "https://efdsearch.senate.gov/api/efs/search"
        self.cache = {}
        self.cache_time = {}
        
    async def fetch_house_trades(self):
        """Fetch recent House member trades"""
        try:
            async with aiohttp.ClientSession() as session:
                # Query for recent disclosures (last 30 days)
                params = {
                    'maxResults': 100,
                    'years': [2026]
                }
                async with session.get(self.house_url, params=params, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self.parse_house_trades(data)
        except Exception as e:
            print(f"House API Error: {e}")
            return []
    
    async def fetch_senate_trades(self):
        """Fetch recent Senate member trades"""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'reportType': 'FD',
                    'year': 2026
                }
                async with session.get(self.senate_url, params=params, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return self.parse_senate_trades(data)
        except Exception as e:
            print(f"Senate API Error: {e}")
            return []
    
    def parse_house_trades(self, data):
        """Parse House disclosure data"""
        trades = []
        try:
            for disclosure in data.get('disclosures', [])[:20]:
                for transaction in disclosure.get('transactions', []):
                    trades.append({
                        'name': disclosure.get('representative', 'Unknown'),
                        'ticker': transaction.get('ticker', 'N/A'),
                        'action': transaction.get('transactionType', 'UNKNOWN'),
                        'value': transaction.get('amount', 'N/A'),
                        'date': transaction.get('transactionDate', datetime.now().isoformat()),
                        'chamber': 'House',
                        'receipt': 'https://disclosures-clerk.house.gov/Public_Disclosure/FinancialDisclosure'
                    })
        except Exception as e:
            print(f"Parse error: {e}")
        return trades
    
    def parse_senate_trades(self, data):
        """Parse Senate disclosure data"""
        trades = []
        try:
            for filing in data.get('filings', [])[:20]:
                for transaction in filing.get('transactions', []):
                    trades.append({
                        'name': filing.get('senatorName', 'Unknown'),
                        'ticker': transaction.get('ticker', 'N/A'),
                        'action': transaction.get('type', 'UNKNOWN'),
                        'value': transaction.get('amount', 'N/A'),
                        'date': transaction.get('date', datetime.now().isoformat()),
                        'chamber': 'Senate',
                        'receipt': 'https://efdsearch.senate.gov/search/'
                    })
        except Exception as e:
            print(f"Parse error: {e}")
        return trades

fetcher = CongressionalDataFetcher()

@app.route('/api/trades', methods=['GET'])
async def get_trades():
    """Get all recent trades"""
    try:
        house_trades = await fetcher.fetch_house_trades()
        senate_trades = await fetcher.fetch_senate_trades()
        
        all_trades = sorted(
            house_trades + senate_trades,
            key=lambda x: x['date'],
            reverse=True
        )
        
        return jsonify({
            'status': 'success',
            'count': len(all_trades),
            'trades': all_trades[:50],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/trades/stream', methods=['GET'])
def stream_trades():
    """Server-Sent Events stream of trades"""
    def generate():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            try:
                house_trades = loop.run_until_complete(fetcher.fetch_house_trades())
                senate_trades = loop.run_until_complete(fetcher.fetch_senate_trades())
                
                trades = (house_trades + senate_trades)[:5]
                
                for trade in trades:
                    yield f"data: {json.dumps(trade)}\n\n"
                
                # Wait before next batch
                loop.run_until_complete(asyncio.sleep(10))
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                loop.run_until_complete(asyncio.sleep(5))
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)