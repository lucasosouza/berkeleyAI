#modelling game of poker

import util
from sets import Set
from util import Stack
from util import Queue
from util import PriorityQueue
from random import random
from random import shuffle
from sets import Set
import time

"""
save two more things:
	tiebraker:
	kicker: 

these will be unique to each strategy
will change the tuple to be a dictionary - easier to work with
better yet - change the tuple to be an object
"""


#########define strategies
def pair(hand):
	for card in hand:
		rHand = list(hand); rHand.remove(card)
		for rCard in rHand:
			if card[0] == rCard[0]:
				s = set([card,rCard])
				kickers = [x for x in hand if x not in s]
				kickers.sort(key=lambda x:x[0])
				kickerScore = kickers[-1]*100 + kickers[-2]*10 + kickers[-3]
				return Play('pair', hand, [card,rCard], card[0], kickerScore)
				#return ('pair', card, rCard)

def triple(hand):
	for card in hand:
		hand1 = list(hand); hand1.remove(card)
		for card in hand1:
			hand2 = list(hand1); hand2.remove(card)
			card1 = hand2[0]; card2 = hand2[1]; card3 = hand2[2]
			if card1[0] == card2[0] == card3[0]:
				s = set([card1, card2, card3])
				kickers = [x for x in hand if x not in s]
				kickers.sort(key=lambda x:x[0])
				kickerScore = kickers[-1]*10 + kickers[-2]*10
				return Play('three of a kind', hand, [card1,card2,card3], card[0], kickerScore)
				#return ('three of a kind', card1, card2, card3)

def quadruple(hand):
	for card in hand:
		hand1 = list(hand); hand1.remove(card)
		card1 = hand1[0]; card2 = hand1[1]; card3 = hand1[2]; card4 = hand1[3]
		if card1[0] == card2[0] == card3[0] == card4[0]:
				s = set([card1, card2, card3, card4])
				kickers = [x for x in hand if x not in s]
				kickerScore = kickers[0][0]
				return Play('four of a kind', hand, [card1, card2, card3, card4], card[0], kickerScore)
				#return ('four of a kind', card1, card2, card3, card4)

def straight(hand):
	originalHand = list(hand) #keeping the original order
	hand.sort(key=lambda x:x[0])
	if hand[0][0] == hand[1][0]-1 == hand[2][0]-2 == hand[3][0]-3 == hand[4][0]-4:
		return Play('straight', originalHand, originalHand, hand[-1][0])
		#return tuple(['straight']) + tuple(hand)

def flush(hand):
	originalHand = list(hand) #keeping the original order
	hand.sort(key=lambda x:x[0])	
	if hand[0][1] == hand[1][1] == hand[2][1] == hand[3][1] == hand[4][1]:
		tieBraker = hand[-2]*1000 + hand[-3]*100 + hand[-4]*10 + hand[-5]
		return Play('flush', originalHand, originalHand, tieBraker)
		#return tuple(['flush']) + tuple(hand)

def straightFlush(hand):
	hStraight = straight(hand)
	if hStraight and flush(hand):
		if hStraight.cards[0] == 10: return Play('royal straight flush', hand, hStraight.tieBraker)
		return Play('straight flush', hand, hand, hStraight.tieBraker)
		#return tuple(['straight flush']) + tuple(hand)		

def fullHouse(hand):
	hTriple = triple(hand)
	if hTriple:
		s = set([hTriple.winningCards[0], hTriple.winningCards[1], hTriple.winningCards[2]])
		#s = set(hTriple.winningCards)
		remaining = [x for x in hand if x not in s] 
		if remaining[0][0] == remaining[1][0]:
			tieBraker = hTriple.winningCards[0][0] * 10 + remaining[0][0]
			return Play('full house', hand, hand, tieBraker)
			#return tuple(['full house']) + tuple(hand)	

def twoPairs(hand):
	firstPair = pair(hand)
	if firstPair:
		s = set([firstPair.winningCards[0], firstPair.winningCards[1]])
		#check for a second pair
		remaining = [x for x in hand if x not in s]
		secondPair = None 
		if remaining[0][0] == remaining[1][0]:
			secondPair = (remaining[0], remaining[1])
		elif remaining[0][0] == remaining[2][0]:
			secondPair = (remaining[0], remaining[2])
		elif remaining[1][0] == remaining[2][0]:
			secondPair = (remaining[1], remaining[2])		
		#return
		if secondPair:
			tieBraker = max(firstPair.winningCards[0][0],secondPair[0][0]) * 10 + min(firstPair.winningCards[0][0],secondPair[0][0])
			s = set([firstPair.winningCards[0], firstPair.winningCards[1], secondPair[0], secondPair[1]])
			kickers = [x for x in hand if x not in s]
			return Play('two pairs', hand, [firstPair.winningCards[0], firstPair.winningCards[1], secondPair[0], secondPair[1]], tieBraker, kickers[0])
			#return tuple(['two pairs']) + tuple(hand)

def highestCard(hand):
	hand.sort(key=lambda x:x[0])
	tieBraker = hand[-2]*1000 + hand[-3]*100 + hand[-4]*10 + hand[-5]
	return Play('highest card', hand, (hand[-1]), tieBraker)
	#return ('highest card', hand[-1])	

##################classes

class Play:
	PLAYS_RANK = {'highest card': 10, 'pair': 9, 'two pairs': 8, 'three of a kind': 7, 'straight': 6, 'flush': 5, 'full house': 4, 'four of a kind': 3, 'straight flush': 2, 'royal straight flush': 1}

	def __init__(self, strategy, cards, winningCards, tieBraker, kicker=None):
		self.strategy = strategy
		self.cards = cards
		self.winningCards = winningCards
		self.tieBraker = tieBraker
		self.kicker = kicker

	def strategy():
		self.strategy

	def tieBraker():
		self.tieBraker

	def kicker():
		self.kicker

	def cards():
		self.cards

	@classmethod
	def winner(cls, plays):
		numberOfPlays = len(plays)
		winner = plays[0]
		for i in range(1, numberOfPlays):
			winner = cls.compare(winner, plays[i])
		return winner

	@classmethod
	def compare(cls, play1, play2, reportTie = None):
		#currently only accounts for two ties
		if isinstance(play1,list): play1adj= play1[0]
		else: play1adj = play1
		#first level comparison
		if cls.PLAYS_RANK[play1adj.strategy] < cls.PLAYS_RANK[play2.strategy]:
			return play1
		elif cls.PLAYS_RANK[play2.strategy] < cls.PLAYS_RANK[play1adj.strategy]:
			return play2
		else:
			#second level comparison
			if play1adj.tieBraker > play2.tieBraker:
				return play1
			elif play2.tieBraker > play1adj.tieBraker:
				return play2
			else:
				#third level comparison
				if play1adj.kicker:
					if play1adj.kicker > play2.kicker:
						return play1
					elif play2.kicker > play1adj.kicker:
						return play2
		#currently only accounts for two ties
		if reportTie:
			return [play1, play2]
		else:
			return play1

class Deck(object):
	SUITS = ['H', 'D', 'S', 'C']
	RANKS = range(2,15)

	def __init__(self):
		self.cards =[] #deck as a list
		for rank in self.RANKS:
			for suit in self.SUITS:
				self.cards.append((rank,suit)) #card as a tuple - numbered 2,14 (ace being 14) - suits H,D,S,C
		self.shuffleDeck()

	def cards(self):
		return self.cards

	def shuffleDeck(self):
		shuffle(self.cards, random)

	def serve(self, n):
		cards = self.cards[0:n]
		del self.cards[0:n]  
		return cards

	def remove(self, selectedCards):
		for card in selectedCards:
			self.cards.remove(card)

class Game(object):

	def __init__(self):
		self.table = []
		self.mainPlayer = None
		self.plays = []
		self.ties = []
		self.deck = Deck()
		self.winner = None

	def run(self, qtdPlayers, cardsAtHand, cardsAtBoard=[]):
		self.start(qtdPlayers, cardsAtHand, cardsAtBoard)
		self.resolve()
		return self.won()

	# def run(self, qtdPlayers, cards):
	# 	self.start(qtdPlayers, cards)
	# 	self.resolve()
	# 	return self.won()

	def start(self, qtdPlayers, cardsAtHand, cardsAtBoard=[]):
		self.deck.remove(cardsAtHand) #remove cards already picken
		self.deck.remove(cardsAtBoard)
		board = self.deck.serve(5-len(cardsAtBoard)) #serve the board
		self.mainPlayer = Player(cardsAtHand + cardsAtBoard + board) #creates the main player and adds to table
		self.table.append(self.mainPlayer)
		for x in range(1, qtdPlayers):
			self.table.append(Player(self.deck.serve(2) + cardsAtBoard + board)) #creates remaining players

	# def start(self, qtdPlayers, cards):
	# 	self.deck.remove(cardsAtHand) #remove cards already picken
	# 	board = self.deck.serve(5) #serve the board
	# 	self.mainPlayer = Player(cards + board) #creates the main player and adds to table
	# 	self.table.append(self.mainPlayer)
	# 	for x in range(1, qtdPlayers):
	# 		self.table.append(Player(self.deck.serve(2) + board)) #creates remaining players

	def resolve(self):
		for player in self.table:
			strategy = player.strategize() #each player create its strategy
			if strategy:
				#print "strategy: ", strategy.strategy, " - ", strategy.cards, " from ", player
				self.plays.append((player, strategy))
		self.pickWinner()

	def pickWinner(self):
		winningHand = Play.winner([x[1] for x in self.plays])
		if isinstance(winningHand, list): #account for many winners - tie
			for hand in winningHand:
				for play in self.plays:
					if play[1] == winningHand:
						self.ties.append(play)
		else: 
			for play in self.plays:
				if play[1] == winningHand:
					self.winner = play 

	def showResult(self):
		if len(self.ties) > 0:
			print "There is a tie between: "
			for tie in ties:
				print tie
		else:			
			print "The winner is: ", self.winner[0]

	def peekPlayers(self):
		for player in self.table:
			print "Player: ", player
			print "Hand: ", player.showCards()

	def won(self):
		if self.winner:
			if self.winner[0] == self.mainPlayer: return True

class Player(object):

	def __init__(self, hand):
		self.hand = hand;
		self.combinations = []
		self.winningPlay = None

	def showCards(self):
		return self.hand

	def strategize(self):
		self.combinations = self.combine(self.hand)
		self.winningPlay = self.solve(self.combinations)
		return self.winningPlay

	#21 possible hand combinations - look for a better way of doing permutation
	def combine(self, hand):
		combinations = []
		for card in hand:
			hand1 = list(hand); hand1.remove(card)
			play1 = []; play1.append(card)
			for card in hand1:
				hand2 = list(hand1); hand2.remove(card)
				play2 = list(play1); play2.append(card)
				for card in hand2:
					hand3 = list(hand2); hand3.remove(card)
					play3 = list(play2); play3.append(card)
					for card in hand3:
						hand4 = list(hand3); hand4.remove(card)
						play4 = list(play3); play4.append(card)
						for card in hand4:
							play5 = list(play4); play5.append(card); play5.sort()
							if play5 not in combinations: combinations.append(play5)
		return combinations	

	#pass all combinations through the strategies
	def solve(self, combinations):
		plays = []
		strategies = (highestCard, pair, twoPairs, triple, straight, flush, fullHouse, quadruple, straightFlush)
		for hand in combinations:
			for strategy in strategies:
				win = strategy(hand)
				if win: plays.append(win)
		return Play.winner(plays); 

#############variables
cardsAtHand = [(7,'C'),(2,'C')]
cardsAtBoard=[]
cardsAtBoard = [(8,'C'),(3,'S'), (9,'H')]
numberOfPlayers = 8

################script to test 
"""
game = Game()
game.start(numberOfPlayers, cards)
game.resolve()
game.showResult()
print game.won()
"""

################script to implement averages
averages = []
start = time.clock()
wins = 0
losses = 0
for y in range(0, 600/numberOfPlayers):
	if Game().run(numberOfPlayers, cardsAtHand, cardsAtBoard): wins += 1
	else: losses += 1
prospect = float(wins)/(wins+losses)
averages.append(prospect)

chanceToWin = reduce(lambda x,y: x+y, averages)/float(len(averages))
print	"Your chance to win is: ", chanceToWin
print	"Your advantage score is: ", chanceToWin/(float(1)/numberOfPlayers)
print "time spent: %f secs" % (time.clock() - start)

#option - prerun all the options - generate a massive json
#how long is it gonna run?
#option 2 - prerun starter options - keep it on json - show as soon as the cards are selected
#2652 -> 21216 from 2 to 9 players

#run on spot for advanced options. have 3 evaluations - a real fast, a intermediate, and a careful slow one



