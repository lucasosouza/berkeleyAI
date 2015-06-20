#arc consistency implementation (with no backtracking) - can solve problems missing 8 numbers only
"""
function AC-3(csp) returns the CSP, possibly with reduced domains
	inputs:csp, a binary CSP with variables {X1,X2,...,Xn}
	local variables: queue, a queue of arcs, initially all the arcs in csp

	while queue is not empty do
		(Xi, Xj) <- REMOVE-FIRST(queue)
		if REMOVE-INCONSISTENT-VALUES(Xi,Xj) then
			for each Xk in NEIGHBORS[Xi] do
				add(Xk, Xi) to queue

function REMOVE-INCONSISTENT-VALUES(Xi, Xj) returns true if succeeds
	removed <- false 
	for each x in DOMAIN[Xi] do
		if no value y in DOMAIN[Xj] allows (x,y) to satisfy the constraint Xi <-> Xj
			then delete x from DOMAIN[Xi]; removed <- true
	return removed
"""
from sys import stdout
from util import Queue as queue

class Game:

	def __init__(self, string):
		self.variables = self.stringToVariables(string)
		self.assignment = {k:v[0] for k,v in self.variables.items() if len(v)==1 }
		self.enforceArcConsistency()

	def enforceArcConsistency(self):
		arcs = queue()
		row = lambda n: n/9
		col = lambda n: n%9 
		box = lambda n: 3*(row(n)/3)+(col(n)/3)
		for var in self.variables:
			neighbors = [k for k in self.variables.keys() if row(var)==row(k) or col(var)==col(k) or box(var)==box(k)]
			for neighbor in neighbors:
				arcs.push((var, neighbor)) #d-squared to push all arcs to the queue
		arcsSize = arcs.size()
		while not arcs.isEmpty():
			if self.completed(): 
				self.prettyPrint()
				return True 
			varA, varB = arcs.pop()
			if (varA in self.assignment.keys()) and (len(self.variables[varB]) > 1):
				if self.removeInconsistentValues(varA, varB):
					neighbors = [k for k in self.variables.keys() if row(varB)==row(k) or col(varB)==col(k) or box(varB)==box(k)]
					for neighbor in neighbors:
						arcs.push((varB, neighbor))
		print "This problem could not be solved with arc-consistency only"
		return False

	def removeInconsistentValues(self, varA, varB):
		removed = False
		for value in self.variables[varB]:
			if value == self.assignment[varA]:
				self.variables[varB].remove(value)
				if len(self.variables[varB]) == 1: 
					self.assignment[varB] = self.variables[varB][0] #assignment
					removed = True
		return removed

	def completed(self):
		return len(self.assignment) == 81

	#end algorithm - start interface
	def prettyPrint(self):
		i = 0
		for w in range (1,4):
			for x in range(1,4):
				for y in range(1,4):
					stdout.write("|")
					for z in range(1,4):
						stdout.write("%d|" % self.assignment[i])
						i+=1
					stdout.write(" ")	
				stdout.write("\n")
			stdout.write("-----------------------\n")

	def stringToVariables(self, string):
		nodes = {index:[int(x)] for index, x in enumerate(list(string.replace("-","0")))}
		for k,v in nodes.items():
			if v==[0]: nodes[k]=[1,2,3,4,5,6,7,8,9]
		return nodes

def solve(string):
	sudoku = Game(string)