from util import Queue as queue
from util import Stack as stack
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
		self.initialState = {x:nodes[x] for x in range(81)}
		self.loops = 0
		self.row = lambda n: n/9
		self.col = lambda n: n%9 
		self.box = lambda n: 3*(self.row(n)/3)+(self.col(n)/3)

	def getInitialState(self): return self.initialState

	def goalChecks(self): return self.loops

	def isGoal(self, state):
		self.loops += 1
		if reduce(lambda x,y: x+y, state.values()) != 405: return False
		for node in state.keys():
			if not self.isValid(state, node): return False
		return True

	def isValid(self, state, node):
		constraints = self.getConstraints(state, node)		
		for cDomain in constraints.values():
			if state[node] == cDomain:
				return False
		return True

	def getConstraints(self, state, node):
		e = {}
		e.update({k:v for k,v in state.items() if self.row(k)==self.row(node) and k!=node}) #row 
		e.update({k:v for k,v in state.items() if self.col(k)==self.col(node) and k!=node}) #col
		e.update({k:v for k,v in state.items() if self.box(k)==self.box(node) and k!=node}) #box
		return e

	def getSuccessors(self, state):
		successors = []
		nextNode = None
		for node, domain in state.items():
			if domain == 0:
				for x in range(1,10):
					successor = dict(state)
					successor[node] = x
					if self.isValid(successor, node):
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
						stdout.write("%d|" % state[i])
						i+=1
					stdout.write(" ")	
				stdout.write("\n")
			stdout.write("-----------------------\n")

#the algorithm to loop
def solve(game):
	problem = Sudoku(game)
	state = problem.getInitialState()
	fringe = queue()
	fringe.push(state)
	while not fringe.isEmpty():
		state = fringe.pop()
		if problem.isGoal(state): 
			print "A solution was found: "
			problem.prettyPrint(state)
			return True
		successors = problem.getSuccessors(state)
		for state in successors:
			fringe.push(state)

	print "There is no solution "
