# Use a Node.js 14 alpine base image
FROM node:14-alpine

# Set the working directory
WORKDIR /app

# Copy the service1.js script into the container
COPY service2.js .

# Install the 'request' library for HTTP requests
RUN npm install request

# Command to run the service
CMD ["sh", "-c", "sleep 2 ; node service2.js"]
