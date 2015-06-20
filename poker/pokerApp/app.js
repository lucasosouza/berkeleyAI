var app = angular.module('pokerCheater', []);

// app.config(function($http){
// 	$http.defaults.headers.common['Authentication']= 'authentication'
// })

app.controller('mainCtrl', function($scope, $http){
	$scope.test = "Input the variable to calculate your win probability";
	$scope.params = {
		players: 6,
		cardsAtHand: [],
		cardsAtTable: []
	}
	$scope.prob = {
		hand: 0,
		table: 0
	}

	//gonna create a card object
	//it will have a numeration

	//create a card model
	function Card(suit, rank, order ){
		this.rank = rank;
		this.suit = suit;
		this.order = order;
		this.selected = {
			hand: false,
			table: false
		};
		this.xPos = ((this.order - 1) % 13) * 50
		this.yPos = Math.floor((this.order-1)/13) * 67.5
	}

	deck = []
	suits = ["Diamonds", "Hearts", "Clubs", "Spades"]
	ranks = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
	order = 1
	for (suit in suits) {
		for (rank in ranks) {
			deck.push(new Card(suits[suit], ranks[rank], order))
			order++;
		}	
	}

	var count = {
		hand: 0,
		table: 0,
		total: function(){
			return this.hand + this.table
		}
	}

	function increase(deckType){
		count[deckType]++
		if ((deckType === "hand" && count[deckType] >= 2) || (deckType === "table" && count[deckType] >= 3)) {
			getStats(deckType)
		}
	}

	function decrease(deckType){
		count[deckType]--
	}

	function updateParams(){
		$scope.params.cardsAtHand = []
		$scope.params.cardsAtTable = []
		for (card in $scope.deck) {
			if ($scope.deck[card].selected.hand) {
				$scope.params.cardsAtHand.push($scope.deck[card].order)
			} else if ($scope.deck[card].selected.table) {
				$scope.params.cardsAtTable.push($scope.deck[card].order)
			}
		}
	}

	$scope.select = function(deck, card) {
		if (count.total() < 2) type = "hand";
		else type = "table";
		for (c in deck){
			if (deck[c] === card) {
				if (deck[c].selected[type]) {
					deck[c].selected[type] = false;
					decrease(type);
				} else { 
					deck[c].selected[type] = true;
					increase(type);
				}
			}
		}
	};

	$scope.deck = deck

	$scope.reset = function(){
		for (card in $scope.deck) {
			$scope.deck[card].selected.hand = false;
			$scope.deck[card].selected.table = false;
		}
		$scope.prob.hand = 0
		$scope.prob.table = 0
		count.hand = 0
		count.table = 0
	}

	function getStats(type){
		if (type === "hand") {
			$scope.params.precision = 4000;
		} else {
			$scope.params.precision = 4000;
		}
		console.log("called get stats");
		updateParams();
		console.log($scope.params);
		$http.post('http://localhost:8124/stats', $scope.params).success(function(data, status, headers){
			console.log(data)
			if (type === "hand") {
				$scope.prob.hand = Number(data);
			} else {
				$scope.prob.table = Number(data);
			}
		})
	}

})

