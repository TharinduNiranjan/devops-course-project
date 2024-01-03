# Use a Python 3.9 alpine base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the service1.py script into the container
COPY service1.py .

# Install dependencies
RUN pip install requests sockets pika tenacity flask

# Command to run the service
CMD ["python", "service1.py"]
