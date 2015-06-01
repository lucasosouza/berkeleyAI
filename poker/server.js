var http = require('http');
var express = require('express');

// http.createServer(function(req,res){
// 	res.writeHead(200, 
// 		{'Content-Type': 'text/plain'});
// 	res.end('Hello Node.js\n')
// }).listen(8124, '127.0.0.1');
// console.log('server running')

//got a server running
//what I need to serve?
//the results of my python file
//there will be many routes?
//if yes, I better get a middleware, unless I want to be doing all the parsing on my own
//no -> get middleware

//ok, installed. let's try this the express way

//will intercept, do something then move to next

//simple server setup
var server = app.listen(8124)

app.use(function(req,res,next){
	console.log('Incoming request');
	next();
});

//routes Incoming
app.get('/test', function(req, res){
	res.status(200).send('oh shit');
});