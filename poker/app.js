var app = angular.module('pokerCheater', []);

app.controller('mainCtrl', function($scope){
	$scope.test = "This is a test";
	$scope.deck = [];
	$scope.cardsAtHand = [];
	$scope.cardsAtTable = [];
	for (var i=1; i< 53;i++ ) {
		$scope.deck.push(i)
	}

})

