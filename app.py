from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

PROM_URL = "http://localhost:9090"

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/status')
def get_status():
    """API endpoint to get current connection status from Prometheus"""
    try:
        print(f"[DEBUG] Querying Prometheus at {PROM_URL}")  # Debug logging
        query = "up"
        response = requests.get(
            f"{PROM_URL}/api/v1/query",
            params={"query": query},
            timeout=5
        )
        
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": f"Prometheus API returned status {response.status_code}",
                "timestamp": datetime.now().isoformat()
            }), 500
        
        data = response.json()
        print(f"[DEBUG] Prometheus response status: {data.get('status')}")  # Debug logging
        print(f"[DEBUG] Number of results: {len(data.get('data', {}).get('result', []))}")  # Debug logging
        
        if data["status"] != "success":
            return jsonify({
                "status": "error",
                "message": "Prometheus query failed",
                "timestamp": datetime.now().isoformat()
            }), 500
        
        # Process results - show all connections, but highlight node2 and node3
        connections = []
        all_instances = []
        
        results = data.get("data", {}).get("result", [])
        print(f"[DEBUG] Processing {len(results)} results")  # Debug logging
        
        for result in results:
            instance = result["metric"].get("instance", "unknown")
            value = result["value"][1]
            is_up = value == "1"
            
            # Collect all instances for debugging
            all_instances.append(instance)
            print(f"[DEBUG] Found instance: {instance}, status: {'up' if is_up else 'down'}")  # Debug logging
            
            # Check if this is node2 or node3
            is_node2_or_3 = "node2" in instance.lower() or "node3" in instance.lower()
            
            connections.append({
                "instance": instance,
                "status": "up" if is_up else "down",
                "value": int(value) if value.isdigit() else 0,
                "is_node23": is_node2_or_3  # Flag to highlight in UI
            })
        
        print(f"[DEBUG] Total connections processed: {len(connections)}")  # Debug logging
        
        # If no results at all, return empty with debug info
        if not connections:
            return jsonify({
                "status": "success",
                "connections": [],
                "timestamp": datetime.now().isoformat(),
                "total_connections": 0,
                "up_connections": 0,
                "debug": {
                    "prometheus_response_status": data.get("status"),
                    "result_count": len(data.get("data", {}).get("result", [])),
                    "all_instances": all_instances
                }
            })
        
        return jsonify({
            "status": "success",
            "connections": connections,
            "timestamp": datetime.now().isoformat(),
            "total_connections": len(connections),
            "up_connections": sum(1 for conn in connections if conn["status"] == "up"),
            "debug": {
                "all_instances": all_instances[:10]  # First 10 for debugging
            }
        })
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            "status": "error",
            "message": "Cannot connect to Prometheus. Please ensure Prometheus is running on localhost:9090",
            "timestamp": datetime.now().isoformat()
        }), 503
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

