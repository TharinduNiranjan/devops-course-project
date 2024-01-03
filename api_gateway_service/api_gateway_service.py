from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

import subprocess



# URLS
MONITOR_SERVICE_URL = "http://monitoring_service:8087"
SERVICE1_URL = "http://service1:8001"
SERVICE2_URL = "http://service2:8002"


def stop_services():
    try:

        response2 = requests.get(f"{SERVICE2_URL}/shutdown")
        response3 = requests.get(f"{MONITOR_SERVICE_URL}/shutdown")
        response1 = requests.put(f"{SERVICE1_URL}/state", data="SHUTDOWN")
        print(response1," ",response2," ",response3)
    except subprocess.CalledProcessError as e:
        print(f"Error stopping services: {e}")



@app.route('/messages', methods=['GET'])
def get_messages():
    # Forward the request to the Monitor service
    response = requests.get(f"{MONITOR_SERVICE_URL}/logs")
    return response.content, response.status_code, {'Content-Type': 'text/plain'}

@app.route('/state', methods=['PUT'])
def set_state():
    new_state = request.get_data().decode('utf-8')
    if new_state == "SHUTDOWN":
        print("shutdown method working")
        stop_services()
        return "shuting down...",200
    else:
        # Forward the request to the service1
        response = requests.put(f"{SERVICE1_URL}/state", data=new_state)
        return response.content, response.status_code, {'Content-Type': 'text/plain'}


@app.route('/state', methods=['GET'])
def get_state():
    # Forward the request to the service1
    response = requests.get(f"{SERVICE1_URL}/state")
    return response.content, response.status_code, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)