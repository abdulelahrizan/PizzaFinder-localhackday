const express = require('express')
const app = express()
const server = require('http').createServer(app);
const port = 3000

app.use(express.static(__dirname + '/site'));
app.get('/', function (req, res, next) {
    res.sendFile(__dirname + '/index.html')
});
server.listen(3000);
console.log("Server started.");