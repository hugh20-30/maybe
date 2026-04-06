# Alpha Tracker Pro - Real-Time Congressional Trading Dashboard

A real-time dashboard built with **PyScript** for monitoring congressional stock trading disclosures from the U.S. House and Senate.

## Features

✅ **Real-time Data Streaming** - Live updates from government APIs  
✅ **PyScript Frontend** - Pure Python in the browser, no JavaScript build tools  
✅ **Congressional Disclosures** - Track House & Senate member trades  
✅ **Win Rate Tracking** - Monitor trader success rates  
✅ **Sector Analysis** - Real-time sector rotation tracking  
✅ **Responsive UI** - Works on desktop and mobile  

## Tech Stack

- **Frontend**: PyScript + HTML/Tailwind CSS
- **Backend**: Flask + aiohttp
- **Data Sources**: 
  - House Clerk's Office API
  - Senate EFD Search API
  - Mock real-time data (for demo)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/hugh20-30/alpha-tracker-realtime.git
cd alpha-tracker-realtime
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Backend Server

```bash
python app.py
```

The backend will start on `http://localhost:5000`

### 4. Open the Frontend

Open `index.html` in your browser (no build step needed!):

```bash
# On macOS
open index.html

# On Linux
firefox index.html

# Or just drag index.html into your browser
```

## API Endpoints

### GET `/api/trades`
Fetch all recent congressional trades

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "trades": [
    {
      "name": "Mark Alford",
      "ticker": "AAPL",
      "action": "SELL",
      "value": "$15K-$50K",
      "date": "2026-04-06T14:30:00",
      "chamber": "House",
      "receipt": "https://..."
    }
  ],
  "timestamp": "2026-04-06T14:35:22"
}
```

### GET `/api/trades/stream`
Server-Sent Events stream for real-time updates

### GET `/api/health`
Health check endpoint

## PyScript Implementation

The frontend uses PyScript to run Python directly in the browser:

```python
# Real-time trade streaming
async def stream_trades(self):
    while True:
        trade = await self.generate_mock_trade()
        self.update_ui(trade)
        await asyncio.sleep(random.uniform(2, 5))
```

No Node.js, no webpack, just Python!

## File Structure

```
alpha-tracker-realtime/
├── index.html           # Main PyScript frontend
├── app.py              # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Real Data Integration

To connect to actual government APIs:

1. **House Clerk's Office**: Modify `fetch_house_trades()` in `app.py`
2. **Senate EFD Search**: Modify `fetch_senate_trades()` in `app.py`
3. Update the API endpoints and parsing logic as needed

## Environment Variables

Create a `.env` file:

```
FLASK_ENV=development
FLASK_DEBUG=True
CORS_ORIGINS=*
```

## Common Issues

### "Cannot find PyScript"
- Make sure you're loading from CDN: `https://pyscript.net/latest/pyscript.js`
- Check browser console for errors

### Backend connection errors
- Ensure `app.py` is running on port 5000
- Check CORS is enabled: `CORS(app)` in Flask

### No real data appearing
- Mock data is enabled by default for demo purposes
- API responses may be delayed; check Network tab in DevTools

## Performance Tips

- Limit trades display to 50 items (implemented)
- Update interval: 2-5 seconds per trade
- Use Server-Sent Events for efficient streaming

## License

Educational use only. See LICENSE file.

## Support

For issues or questions:
📧 hughvanatta@treynorcardinals.org

---

**Disclaimer**: This is an educational tool for tracking public congressional disclosures. Not financial advice. Always conduct your own research.