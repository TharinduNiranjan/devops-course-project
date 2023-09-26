const http = require('http');
const fs = require('fs');

fs.writeFileSync('/logs/service2.log', ''); //set initial file content to blank
const server = http.createServer((req, res) => {
  if (req.method === 'POST') {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
    });
    req.on('end', () => {
      if (data === 'STOP') {
        res.statusCode=200;
        res.end("OK");
        fs.closeSync(service2Log);  // Close service2.log and exit
        process.exit(0);
      } else {
        const remoteAddress = req.socket.remoteAddress + ':' + req.socket.remotePort;
        const logEntry = `${data} ${remoteAddress}`;
        fs.appendFileSync('/logs/service2.log', logEntry + '\n'); // append data to the service2 file
        res.statusCode=200;
        res.end();
      }
    });
  }
});

const service2Log = fs.openSync('/logs/service2.log', 'a'); //opening the service2 file in append mode

//start the server with 8000 port
server.listen(8000, () => {
  console.log('Service 2 is listening on port 8000');
});