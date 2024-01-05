# Use a Python 3.9 alpine base image
FROM python:3.9-alpine

RUN apk add docker
# Set the working directory
WORKDIR /app

# Copy the api_gateway_service.py script into the container
COPY api_gateway_service.py .

# Copy the test_api_gateway_service.py script into the container
COPY tests/test_api_gateway_service.py .

# Install dependencies
RUN pip install requests flask python-http-client pybase64

# Command to run the service
CMD ["python", "api_gateway_service.py"]