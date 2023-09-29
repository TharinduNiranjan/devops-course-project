# Use a Python 3.9 alpine base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the service2.py script into the container
COPY service1.py .

# Install Flask for the web server
RUN pip install requests sockets

# Command to run the service
CMD ["python", "service1.py"]
