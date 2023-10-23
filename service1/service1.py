
#Import libraries 
import requests
import datetime
import socket
import pika
import time

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

#declaring message queue
channel.queue_declare(queue='message')

#declaring message queue
channel.queue_declare(queue='log')

count = 1 # set initial count to 1
remote_host = 'service2' # to get the remote host address through docker network
remote_host_ip = socket.gethostbyname(remote_host) # get the service2 ip


for _ in range(20):
    time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ") # get time stamp
    data = f"SND {count} {time_stamp} {remote_host_ip}:8000"  # construct text data to send and write

    # Send message to RabbitMQ
    print("sending data to rabbitmq "+data)
    channel.basic_publish(exchange='', routing_key='message', body=data)

    # Send HTTP request to Service 2
    service2_url = "http://service2:8000"
    try:
        print("sending data to service2 "+data)
        response = requests.post(service2_url, data=data)
        print(response.status_code)
        # Process response and send log to RabbitMQ
        if response.status_code == 200:
            response_timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_data = f"200 {response_timestamp}"
        else:
            log_data = f"{response.status_code} {response_timestamp}"
        channel.basic_publish(exchange='', routing_key='log', body=log_data)
    except Exception as e:
             error_message = f'Error: {str(e)}'
             print(error_message)
             channel.basic_publish(exchange='', routing_key='log', body=error_message)
    time.sleep(2)  # to set a 2 second delay
    count += 1

# Send STOP signal to RabbitMQ
print("sending stop message to log queue")
channel.basic_publish(exchange='', routing_key='log', body="SND STOP")

# Close the RabbitMQ connection
connection.close()

# Wait for the operator to issue the "docker compose down" command
while True:
    time.sleep(1)