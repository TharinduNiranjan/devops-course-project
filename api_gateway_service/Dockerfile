# Use a Python 3.9 alpine base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /app

# Copy the api_gateway_service.py script into the container
COPY api_gateway_service.py .
COPY tests/test_api_gateway_service.py .
# Install dependencies
RUN pip install requests flask

# Command to run the service
CMD ["python", "api_gateway_service.py"]