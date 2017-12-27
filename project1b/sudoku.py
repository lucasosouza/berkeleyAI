from util import Queue as queue
from util import Stack as stack
import random


#problem: keep track of numbers already tried, so I won't try them again
#has to be recursive. I'm not so sure on recursive
#alternative: try and understand the AC3 algorithm and implement

#using standard search
#state -> values assigned so far. initial state -> []
#successor function: assign a variable
#goal test: current assignment satisfies all constraints

#let's start with the naive approach, meaning no arc-consistency

###########################dummy way - no filter

class Sudoku:

	def __init__(self):
		self.initialState = {x:0 for x in range(81)}
		self.costFn = lambda x: 1

	def getConstraints(self, node,state):
		e = {}
		row = lambda n: n/9
		col = lambda n: n%9 
		box = lambda n: 3*(row(n)/3)+(col(n)/3)
		e.update({k:v for k,v in state.items() if row(k)==row(node) and k!=node}) #row 
		e.update({k:v for k,v in state.items() if col(k)==col(node) and k!=node}) #col
		e.update({k:v for k,v in state.items() if box(k)==box(node) and k!=node}) #box
		return e

	def isGoal(self, state):
		for node in state.keys():
			constraints = self.getConstraints(node, state)
			for cDomain in constraints.values():
				if state[node] == cDomain:
					return False
		return True

	def getSuccessors(self, state):
		successors = []
		for node, domain in state.items():
			if domain == 0:
				nextNode = node
				break
		for x in range(1,10):
			successor = dict(state)
			successor[node] = x
			successors.append(successor)
		return successors

#the algorithm to loop
def solve(problem):
	state = problem.initialState
	fringe = queue()
	fringe.push(state)
	while not fringe.isEmpty():
		state = fringe.pop()
		if problem.isGoal(state): 
			print "A solution was found: ", "".join(state)
			return True
		for state in problem.getSuccessors(state):
			fringe.push(state)

	print "There is no solution "

solve(Sudoku())


