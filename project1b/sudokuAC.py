from util import Queue as queue
from util import Stack as stack
import random
import time
from sys import stdout

#problem: keep track of numbers already tried, so I won't try them again
#has to be recursive. I'm not so sure on recursive
#alternative: try and understand the AC3 algorithm and implement

#using standard search
#state -> values assigned so far. initial state -> []
#successor function: assign a variable
#goal test: current assignment satisfies all constraints

#let's start with the naive approach, meaning no arc-consistency

########################### less dummy way - forward looking filter

class Sudoku:

	def __init__(self, string):
		nodes = [int(x) for x in list(string.replace("-","0"))]
		nodesA = map(lambda x: [1,2,3,4,5,6,7,8,9] if x == 0 else [x], nodes)
		self.initialState = {x:nodesA[x] for x in range(81)}
		self.loops = 0
		self.row = lambda n: n/9
		self.col = lambda n: n%9 
		self.box = lambda n: 3*(self.row(n)/3)+(self.col(n)/3)

	def getInitialState(self): return self.initialState

	def goalChecks(self): return self.loops

	def isGoal(self, state):
		self.loops += 1
		#only one value
		solved = len([x for x in state.values() if len(x) == 1])
		print solved
		if solved != 81: return False 
		#they all must sum 405
		if reduce(lambda x,y: x+y[0], state.values(), 0) != 405: return False
		#they should follow the specified constraints - (later)
		# for node in state.keys():
		# 	if not self.isValid(state, node): return False
		return True

	def enforceArcConsistency(self,state,node):
		arcsToValidate = queue()
		arcsToValidate.push(node)
		while not arcsToValidate.isEmpty():
			node = arcsToValidate.pop()
			connections = self.getConnections(state, node)
			for connection in connections.keys():
				if len(state[connection]) > 1:
					for valueC in state[connection]:
						if valueC == state[node][0]:
							state[connection].remove(valueC)
							#print "connections", len(state[connection])
							if len(state[connection]) == 0:
								#print "breaking"
								return False
							elif len(state[connection]) == 1:
								arcsToValidate.push(connection)

		#after all the iterations, return the state
		#print "state size", reduce(lambda x,y: x+len(y), state.values(), 0)
		return state

	def validate(self,state,node):
		connections = self.getConnections(state, node)
		for connection in connections.keys():
			if len(state[connection]) == 1:
				if state[connection][0] == state[node][0]:
					print "connection", state[connection]
					print "node", state[node]
					return False
		return state

	def getConnections(self, state, node):
		e = {}
		e.update({k:v for k,v in state.items() if self.row(k)==self.row(node) and k!=node}) #row 
		e.update({k:v for k,v in state.items() if self.col(k)==self.col(node) and k!=node}) #col
		e.update({k:v for k,v in state.items() if self.box(k)==self.box(node) and k!=node}) #box
		return e

	def getSuccessors(self, state):
		successors = []
		for node, domain in state.items():
			if len(domain) > 1:
				#print "node", node
				#print "domain", domain
				for x in domain:
					successor = dict(state)
					successor[node] = [x]
					#print "successor", successor[node]
					successor = self.validate(successor, node) 
					if successor:
						successor = self.enforceArcConsistency(successor, node)
					if successor:
						successors.append(successor)
				break

		return successors

	def prettyPrint(self, state):
		i = 0
		for w in range (1,4):
			for x in range(1,4):
				for y in range(1,4):
					stdout.write("|")
					for z in range(1,4):
						stdout.write("%d|" % state[i][0])
						i+=1
					stdout.write(" ")	
				stdout.write("\n")
			stdout.write("-----------------------\n")

#the algorithm to loop
def solve(problem):
	state = problem.getInitialState()
	fringe = stack()
	fringe.push(state)
	visitedStates = set()
	while not fringe.isEmpty():
		#visitedStates.add("-".join(state.values()))
		#print "fringe size", fringe.size()
		state = fringe.pop()
		if problem.isGoal(state): 
			print "A solution was found: "
			problem.prettyPrint(state)
			return True
		if str(state) not in visitedStates:
			visitedStates.add(str(state))
			successors = problem.getSuccessors(state)
				#print len(successors)
			for state in successors:
				fringe.push(state)

	print "There is no solution "

#############runner
def run(index, game, totalTime):
	start = time.clock()
	sudoku = Sudoku(game)
	print "Game number: %d" % index 
	solve(sudoku)
	timeSpent = (time.clock() - start)
	totalTime += timeSpent
	print "Time elapsed: %f secs" % timeSpent
	print "Goal checks: %d" % sudoku.goalChecks()
	print "\n"
	return totalTime

source = """-96-4---11---6---45-481-39---795--43-3--8----4-5-23-18-1-63--59-59-7-83---359---7"""
#35 numeros - ainda acha solucao
#menos - nao acha 

games = source.split("\n")
totalTime = 0
for index, game in enumerate(games): 
	totalTime += run(index, game, totalTime)
print "****** Total time elapsed: %f secs" % totalTime
