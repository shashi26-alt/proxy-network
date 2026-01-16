# Node Connections Dashboard

A modern web-based dashboard for monitoring connections from Node2 and Node3 via Prometheus metrics.

## Features

- 🎨 Modern, responsive web interface
- 🔄 Real-time auto-refresh (every 5 seconds)
- 📊 Statistics overview (Total, Active, Down connections)
- ✅ Visual status indicators with color coding
- 🌐 Accessible via web browser

## Prerequisites

- Python 3.7+
- Prometheus running on `http://localhost:9090`
- Prometheus metrics available for node2 and node3 instances

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Ensure Prometheus is running on `http://localhost:9090`
2. Start the Flask application:
```bash
python app.py
```

3. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

- `app.py` - Flask backend application with API endpoints
- `templates/dashboard.html` - Web dashboard UI
- `requirements.txt` - Python dependencies
- `test.py` - Original script (kept for reference)

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/status` - JSON API endpoint for connection status

## Notes

- The dashboard automatically filters and displays connections from node2 and node3
- Connection status is refreshed every 5 seconds automatically
- The dashboard will show an error message if Prometheus is not accessible

# proxy-network
