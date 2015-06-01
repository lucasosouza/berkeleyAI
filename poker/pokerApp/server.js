//var http = require('http');
var express = require('express');
var app = express();
var databaseUrl = "pokerStats";
var collections = ["plays"]
var db = require("mongojs").connect(databaseUrl, collections)
var bodyParser = require('body-parser')

//shell level interactions
var sys = require("sys")
var exec = require("child_process").exec;

//is body parser still required? not sure

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

//parse post request
app.use(bodyParser.json());

//handlers CORS
app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

//test is working
//routes Incoming
app.get('/test', function(req, res){
	res.status(200).send('oh shit');
});

app.post('/stats', function(req, res){
	console.log(req.body)
	command = "python poker.py -p "
	command += req.body.players
	command += (" -pr " + req.body.precision)
	for (card in req.body.cardsAtHand) {
		command += (" -c " + req.body.cardsAtHand[card])		
	}
	for (card in req.body.cardsAtTable) {
		command += (" -t " + req.body.cardsAtTable[card])		
	}
	console.log(command)
	exec(command, function(error, stdout, stderr){
		res.setHeader('Content-Type', 'text/plain')
		res.status(200).send(stdout);		
	})
});

// function getStats(qtdPlayers){

// }

// function handle(error, stdout, stderr){
// 	//sys.puts(stdout);

// }

//examples
// var mongojs = require("mongojs");
// var ObjectId = mongojs.ObjectId;
// var databaseUrl = "mymoneydb";
// var collections = ["expenses", "items", "incomes", "budgets", "mortgages"]
// var db = mongojs.connect(databaseUrl, collections)

// db.expenses.find(function(err, data){
// 	deferred.resolve(data)
// })
// return deferred.promise 
// return db.expenses.insert(obj);
// return db.expenses.remove(query)
// return db.expenses.update(id_to_update, obj)
// return db.expenses.find(query);
// return db.expenses.drop();

