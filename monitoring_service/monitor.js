const http = require('http');
const amqp = require('amqp-connection-manager');

// defining arrays to store received messages from RabbitMQ
const receivedMessages = [];
const receivedRunLogMessages = [];

const connection = amqp.connect(['amqp://rabbitmq']);

 // Consume messages from RabbitMQ "log" topic and forward to "log-state" topic

const channelWrapper = connection.createChannel({
  json: true,
  setup: (channel) => {
    const queue = 'log';

    channel.assertQueue(queue, { durable: false });
    channel.consume(queue, (msg) => {
      receivedMessages.push(msg.content.toString());
    }, { noAck: true });

    const queueRunLog = 'log-state';

    channel.assertQueue(queueRunLog, { durable: false });
    channel.consume(queueRunLog, (msg) => {
      receivedRunLogMessages.push(msg.content.toString());
    }, { noAck: true });
    console.log('Waiting for log messages from RabbitMQ...');
  },
});

// Function to run HTTP server and handle incoming requests
function runHttpServer() {
  const server = http.createServer((req, res) => {
    if (req.url === '/logs') {
      res.setHeader('Content-Type', 'text/plain');
      res.end(receivedMessages.join('\n'));
    } else if(req.url === '/run-logs'){
      res.setHeader('Content-Type', 'text/plain');
      res.end(receivedRunLogMessages.join('\n'));
    } else {
      res.statusCode = 404;
      res.end('Not Found');
    }
  });

  server.listen(8087, () => {
    console.log('Monitoring service is running on port 8087');
  });
}

 // Attempt to connect to RabbitMQ
connection.on('connect', () => {
  console.log('Connected to RabbitMQ');
  runHttpServer();
});

connection.on('disconnect', (params) => {
  console.error('Disconnected from RabbitMQ. Retrying...');
  channelWrapper.close();
  setTimeout(() => connection.reconnect(), 5000);
});
