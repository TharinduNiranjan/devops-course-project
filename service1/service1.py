#Import libraries
import requests
import datetime
import socket
import pika
import time
import threading
import os
from flask import Flask, jsonify, request

from tenacity import retry, stop_after_delay, wait_fixed


@retry(stop=stop_after_delay(30), wait=wait_fixed(2))
def connect_to_rabbitmq():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        print("connected..")
        return connection
    except pika.exceptions.AMQPConnectionError:
        print("Failed to connect to RabbitMQ. Retrying...")
        raise  # Raise the exception to trigger the retry

# Attempt to connect to RabbitMQ


connection = connect_to_rabbitmq()
channel = connection.channel()

#  declaring log-state queue
channel.queue_declare(queue='log-state')

#  declaring message queue
channel.queue_declare(queue='message')

#  declaring log queue
channel.queue_declare(queue='log')

# Define the remote host and its IP address
remote_host = 'service2'  # to get the remote host address through docker network
remote_host_ip = socket.gethostbyname(remote_host) # get the service2 ip
running_state = False
previous_state= None
max_rounds = 20
current_round = 0
counter = 1
lock = threading.Lock()
service2_url = "http://service2:8002"
monitoring_service_url="http://monitoring_service:8087"

# Function to send messages to RabbitMQ and Service 2
def send_messages():
    global counter,remote_host_ip,service2_url
    time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # get time stamp
    data = f"SND {counter} {time_stamp} {remote_host_ip}:8002"  # construct text data to send and write

    # Send message to RabbitMQ
    print("sending data to rabbitmq " + data)
    channel.basic_publish(exchange='', routing_key='message', body=data)
    # Send HTTP request to Service 2
    try:
        print("sending data to service2 " + data)
        response = requests.post(service2_url, data=data)
        print(response.status_code)
        # Process response and send log to RabbitMQ
        response_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if response.status_code == 200:
            log_data = f"200 {response_timestamp}"
        else:
            log_data = f"{response.status_code} {response_timestamp}"
        channel.basic_publish(exchange='', routing_key='log', body=log_data)
    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        channel.basic_publish(exchange='', routing_key='log', body=error_message)


def loop_function():
    global running_state, counter, previous_state
    while True:
        with lock:
            if running_state and counter <= max_rounds:
                send_messages()
                counter += 1
            elif counter > max_rounds:
                running_state = False  # Pause the loop after all messages have been sent
        time.sleep(2)

# Create a thread for the loop function
loop_thread = threading.Thread(target=loop_function)

# Start the loop thread
loop_thread.start()

app = Flask(__name__)

# Endpoint to update the system state
@app.route('/state', methods=['PUT'])
def update_state():
    global running_state, counter, previous_state
    print(request.data)
    new_state = request.data.decode('utf-8')

    with lock:
        if new_state == "RUNNING" and counter ==1:
            return jsonify(f"Please initiate system before run"), 200


        if new_state == previous_state:
            return jsonify( f"State is already {new_state}"), 200

        # send status change into rabbitmq
        time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")  # get time stamp
        state_change = f"{time_stamp}: {previous_state} -> {new_state}"
        print("sending data to rabbitmq " + state_change)
        channel.basic_publish(exchange='', routing_key='log-state', body=state_change)

        # Handle different state transitions
        if new_state == "INIT":
            counter = 1
            previous_state = "RUNNING"
            running_state = True
        elif new_state == "PAUSED":
            running_state = False
            previous_state="PAUSED"
        elif new_state == "RUNNING":
            previous_state="RUNNING"
            running_state = True
        elif new_state == "SHUTDOWN":
            running_state=False
            previous_state = "SHUTDOWN"
            # Send STOP signal to RabbitMQ
            print("sending stop message to log queue")
            channel.basic_publish(exchange='', routing_key='log', body="SND STOP")
            # Close the RabbitMQ connection
            connection.close()
            return jsonify({"status changed"}), 200
        else:
            return jsonify(f"{new_state} not found"), 200

    return jsonify(f"State updated to {new_state}"), 200

# Endpoint to get the current system state
@app.route('/state', methods=['GET'])
def get_state():
    global previous_state
    return previous_state

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8001)





