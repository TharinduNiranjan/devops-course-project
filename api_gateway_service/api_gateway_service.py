from flask import Flask, request, jsonify
import requests
import subprocess
import threading

app = Flask(__name__)

# URLS
MONITOR_SERVICE_URL = "http://monitoring_service:8087"
SERVICE1_URL = "http://service1:8001"


def stop_services():
    try:
        container_ids = subprocess.check_output(['docker', 'ps', '-q']).decode('utf-8').splitlines()
        subprocess.run(['docker', 'stop'] + container_ids)
    except Exception as e:
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
        try:
            response = requests.put(f"{SERVICE1_URL}/state", data=new_state)
            print(response.content)
            threading.Thread(target=stop_services).start()
            return "services stopped..", response.status_code, {'Content-Type': 'text/plain'}
        except Exception as e:
            return jsonify(f"Error:{e}", 500)
    else:
        # Forward the request to the service1
        response = requests.put(f"{SERVICE1_URL}/state", data=new_state)
        return response.content, response.status_code, {'Content-Type': 'text/plain'}


@app.route('/state', methods=['GET'])
def get_state():
    # Forward the request to the service1
    response = requests.get(f"{SERVICE1_URL}/state")
    return response.content, response.status_code, {'Content-Type': 'text/plain'}

@app.route('/run-log', methods=['GET'])
def get_run_log():
    # Forward the request to the Monitor service
    response = requests.get(f"{MONITOR_SERVICE_URL}/run-logs")
    return response.content, response.status_code, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)