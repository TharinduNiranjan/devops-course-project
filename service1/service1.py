
#Import libraries 
import requests
import datetime
import socket
import time

count = 1 # set initial count to 1
remote_host = 'service2' # to get the remote host address through docker network
remote_host_ip = socket.gethostbyname(remote_host) # get the service2 ip
with open('/logs/service1.log', 'w') as log_file:
    for _ in range(20):
        time_stamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ") # get time stamp
        
        text = f"{count} {time_stamp} {remote_host_ip}:8000"  # construct text data to send and write
        
        # Write to service1.log
        log_file.write(text + '\n')    # write the data into a text file

        try:
            # Send the text with HTTP to service2
            response = requests.post('http://service2:8000', data=text) # send the request to service2
            if response.status_code != 200:
                log_file.write(f"Error: {response.status_code} - {response.text}\n")
        except Exception as e:
            log_file.write(f"Error: {str(e)}\n") # handling the exception
        time.sleep(2)  # to set a 2 second delay
        count += 1 # increase the count

   
    log_file.write("STOP")  # Write "STOP" to service1.log

try:
    response = requests.post('http://service2:8000', data="STOP") # send stop request to service2
    print(response.text)
except Exception as e:
    print (f"Error: {str(e)}") # handling the exception