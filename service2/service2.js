const http = require('http');
const amqp = require('amqplib/callback_api');

const startService = () => {
  const server = http.createServer((req, res) => {
    if (req.method === 'POST') {
      let data = '';
      req.on('data', (chunk) => {
        data += chunk;
      });
      req.on('end', () => {
        const remoteAddress = req.connection.remoteAddress + ':' + req.connection.remotePort;
        const logEntry = `${data} ${remoteAddress}`;

        // Send log to RabbitMQ
        amqp.connect('amqp://rabbitmq', (error, connection) => {
          if (error) {
            console.error('Error connecting to RabbitMQ:', error);
            return;
          }

          connection.createChannel((error, channel) => {
            if (error) {
              console.error('Error creating RabbitMQ channel:', error);
              return;
            }

            const queue = 'log';
            channel.assertQueue(queue, { durable: false });
            channel.sendToQueue(queue, Buffer.from(logEntry));
            console.log('Sent to RabbitMQ:', logEntry);
          });
        });

        res.statusCode = 200;
        res.end('OK');
      });
    } else if (req.url === '/shutdown') {
      // Handle shutdown request
      shutdownService(res);

    }
  });

  server.listen(8002, () => {
    console.log('Service 2 is listening on port 8000');
  });

  // Consume messages from RabbitMQ "message" topic and forward to "log" topic
  amqp.connect('amqp://rabbitmq', (error, connection) => {
    if (error) {
      console.error('Error connecting to RabbitMQ for consumption:', error);
      return;
    }

    connection.createChannel((error, channel) => {
      if (error) {
        console.error('Error creating RabbitMQ channel for consumption:', error);
        return;
      }

      const messageQueue = 'message';
      const logQueue = 'log';

      channel.assertQueue(messageQueue, { durable: false });
      channel.assertQueue(logQueue, { durable: false });

      channel.consume(messageQueue, (message) => {
        if (message.content) {
          const receivedMessage = message.content.toString();
          const logEntry = `${receivedMessage} MSG`;

          // Send the modified log entry to the "log" topic
          channel.sendToQueue(logQueue, Buffer.from(logEntry));
          console.log('Forwarded to "log" topic:', logEntry);
        }
      });
    });
  });
};

const shutdownService = (res) => {
  console.log('Shutting down Service 2...');
  // Close the server and exit the process
  res.statusCode = 200;
  res.end('Shutting down Service 2...');
  process.exit(0);
};

const waitForRabbitMQ = () => {
  amqp.connect('amqp://rabbitmq', (error, connection) => {
    if (error) {
      console.error('Waiting for RabbitMQ...');
      setTimeout(waitForRabbitMQ, 5000); // Retry after 5 seconds
    } else {
      console.log('RabbitMQ is ready.');
      startService();
    }
  });
};

waitForRabbitMQ();
