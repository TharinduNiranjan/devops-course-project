# Use a Node.js 14 alpine base image
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy the service2.js script into the container
COPY monitor.js .

# Install the 'http' library for HTTP requests
RUN npm install http amqplib amqp-connection-manager

# Command to run the service
CMD ["sh", "-c", "sleep 2 ; node monitor.js"]