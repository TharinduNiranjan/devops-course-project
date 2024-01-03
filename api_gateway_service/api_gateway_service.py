from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

import subprocess



# URLS
MONITOR_SERVICE_URL = "http://monitoring_service:8087"
SERVICE1_URL = "http://service1:8001"
SERVICE2_URL = "http://service2:8002"





@app.route('/messages', methods=['GET'])
def get_messages():
    # Forward the request to the Monitor service
    response = requests.get(f"{MONITOR_SERVICE_URL}/logs")
    return response.content, response.status_code, {'Content-Type': 'text/plain'}



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)