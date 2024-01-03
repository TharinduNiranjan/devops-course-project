const http = require('http');
const amqp = require('amqp-connection-manager');

const receivedMessages = [];

const connection = amqp.connect(['amqp://rabbitmq']);
const channelWrapper = connection.createChannel({
  json: true,
  setup: (channel) => {
    const queue = 'log';

    channel.assertQueue(queue, { durable: false });
    channel.consume(queue, (msg) => {
      receivedMessages.push(msg.content.toString());
    }, { noAck: true });

    console.log('Waiting for log messages from RabbitMQ...');
  },
});

function runHttpServer() {
  const server = http.createServer((req, res) => {
    if (req.url === '/logs') {
      res.setHeader('Content-Type', 'text/plain');
      res.end(receivedMessages.join('\n'));
    } else {
      res.statusCode = 404;
      res.end('Not Found');
    }
  });

  server.listen(8087, () => {
    console.log('Monitoring service is running on port 8087');
  });
}

connection.on('connect', () => {
  console.log('Connected to RabbitMQ');
  runHttpServer();
});

connection.on('disconnect', (params) => {
  console.error('Disconnected from RabbitMQ. Retrying...');
  channelWrapper.close();
  setTimeout(() => connection.reconnect(), 5000);
});
