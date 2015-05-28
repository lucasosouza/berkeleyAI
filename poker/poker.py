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

class Deck(object):
	SUITS = ['H', 'D', 'S', 'C']
	RANKS = range(2,14)

	def __init__(self):
		self.cards =[] #deck as a list
		for rank in RANKS:
			for suit in SUITS:
				self.cards.append((rank,suit)) #card as a tuple - numbered 2,14 (ace being 14) - suits H,D,S,C

	def shuffleDeck():
		shuffle(self.cards, random)

	def serve(n):
		self.cards.pop(n)

	def remove(selectedCards):
		for card in selectedCards:
			self.cards.remove(card)

class Game(object):

	def __init__(self):
		self.players = []

	def start(qtdPlayers, cards):
		deck = Deck()
		deck.remove(cards)
		board = deck.serve(5)
		main = Player(cards + board)
		self.players.append(main)
		for x in range(a, qtdPlayers):
			self.players.append(Player(deck.serve(2) + board))

	def resolve():
		for player in self.players:
			player.strategize()
		winning = PriorityQueue()
		for player in players

class Player(object):

	def __init__(self, hand):
		self.hand = hand;
		self.combinations = []
		self.winningPlay = None

	def strategize():
		self.combinations = combine(self.hand)
		self.winningPlay = solve(self.combinations)
		return self.winningPlay

	#21 possible hand combinations - look for a better way of doing permutation
	def combine(hand):
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
	def solve(combinations):
		plays = PriorityQueue()
		for hand in combinations:
			winStraightFlush = straightFlush(hand)
			if winStraightFlush: plays.push(winStraightFlush, 2)
			winQuadruple = quadruple(hand)
			if winQuadruple: plays.push(winQuadruple,3)
			winFullHouse = fullHouse(hand)
			if winFullHouse: plays.push(winFullHouse, 4)
			winFlush = flush(hand)
			if winFlush: plays.push(winFlush, 5)		
			winStraight = straight(hand)
			if winStraight: plays.push(winStraight, 6)
			winTriple = triple(hand) 
			if winTriple: plays.push(winTriple, 7)
			winTwoPairs = twoPairs(hand)
			if winTwoPairs: plays.push(winTwoPairs, 8)
			winPair = pair(hand)
			if winPair: plays.push(winPair, 9)
		if not plays.isEmpty(): 
			winningPlay = plays.pop()
			return winningPlay; 



#define strategies
def pair(hand):
	for card in hand:
		rHand = list(hand); rHand.remove(card)
		for rCard in rHand:
			if card[0] == rCard[0]:
				return ('pair', card, rCard)

def triple(hand):
	for card in hand:
		hand1 = list(hand); hand1.remove(card)
		for card in hand1:
			hand2 = list(hand1); hand2.remove(card)
			card1 = hand2[0]; card2 = hand2[1]; card3 = hand2[2]
			if card1[0] == card2[0] == card3[0]:
				return ('three of a kind', card1, card2, card3)

def quadruple(hand):
	for card in hand:
		hand1 = list(hand); hand1.remove(card)
		card1 = hand1[0]; card2 = hand1[1]; card3 = hand1[2]; card4 = hand1[3]
		if card1[0] == card2[0] == card3[0] == card4[0]:
				return ('four of a kind', card1, card2, card3, card4)

def straight(hand):
	hand.sort(key=lambda x:x[0])
	if hand[0][0] == hand[1][0]-1 == hand[2][0]-2 == hand[3][0]-3 == hand[4][0]-4:
		return tuple(['straight']) + tuple(hand)

def flush(hand):
	if hand[0][1] == hand[1][1] == hand[2][1] == hand[3][1] == hand[4][1]:
		return tuple(['flush']) + tuple(hand)

def straightFlush(hand):
	hStraight = straight(hand)
	if hStraight and flush(hand):
		if hStraight[1][0] == 10: return tuple(['royal straight flush']) + tuple(hand)	
		return tuple(['straight flush']) + tuple(hand)		

def fullHouse(hand):
	hTriple = triple(hand)
	if hTriple:
		s = set([hTriple[1], hTriple[2], hTriple[3]])
		remaining = [x for x in hand if x not in s] 
		if remaining[0][0] == remaining[1][0]:
			return tuple(['full house']) + tuple(hand)	

def twoPairs(hand):
	hPair = pair(hand)
	if hPair:
		s = set([hPair[1], hPair[2]])
		remaining = [x for x in hand if x not in s] 
		if remaining[0][0] == remaining[1][0] or remaining[0][0] == remaining[2][0] or remaining[1][0] == remaining[2][0]:
			return tuple(['two pairs']) + tuple(hand)	

















# #calculates the probability
# def calcProb():
# 	start = time.clock()
# 	wins = 0; losses = 0;
# 	for x in range(0,10000):
# 		if solve(combine(serve(game()))): 
# 			wins += 1
# 		else: 
# 			losses += 1

# 	print "wins: ", wins
# 	print "losses: ", losses
# 	print "prob: ", float(wins*100)/(wins+losses)
# 	print "time spent: %f secs" % (time.clock() - start)

# calcProb()




