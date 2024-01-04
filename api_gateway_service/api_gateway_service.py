from flask import Flask, request, jsonify
import requests
import subprocess
import threading
import http
import base64
app = Flask(__name__)

# URLS
MONITOR_SERVICE_URL = "http://monitoring_service:8087"
SERVICE1_URL = "http://service1:8001"

# URLS
MONITOR_SERVICE_URL = "http://monitoring_service:8087"
SERVICE1_URL = "http://service1:8001"
SERVICE2_URL = "http://service2:8002"

# RabbitMQ API URLs
RABBITMQ_HOST = 'rabbitmq'
RABBITMQ_PORT = 15672
RABBITMQ_API_URL = f'/api'

# RabbitMQ credentials
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'

# Function to fetch RabbitMQ statistics
def get_rabbitmq_statistics():
    try:
        # Create a connection to RabbitMQ API
        connection = http.client.HTTPConnection(RABBITMQ_HOST, RABBITMQ_PORT)

        # Encode credentials for authentication
        credentials = base64.b64encode(f'{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}'.encode('utf-8')).decode('utf-8')

        # Set headers for authentication
        headers = {'Authorization': f'Basic {credentials}'}

        # Fetch overall statistics
        connection.request('GET', f'{RABBITMQ_API_URL}/overview', headers=headers)
        overall_response = connection.getresponse()
        overall_statistics = overall_response.read().decode('utf-8')

        # Fetch per-queue statistics
        connection.request('GET', f'{RABBITMQ_API_URL}/queues', headers=headers)
        queues_response = connection.getresponse()
        queues_statistics = queues_response.read().decode('utf-8')

        # Close the connection
        connection.close()

        return {
            'overall': overall_statistics,
            'queues': queues_statistics
        }

    except Exception as e:
        return str(e)

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

@app.route('/mqstatistic', methods=['GET'])
def get_mq_statistics():
    # Forward the request to get RabbitMQ statistics
    rabbitmq_statistics = get_rabbitmq_statistics()
    return rabbitmq_statistics, 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083)