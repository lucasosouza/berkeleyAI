#arc consistency implementation with backtracking
from sys import stdout
from util import Queue as queue

class Game:

	def __init__(self, string):
		self.variables = self.stringToVariables(string)
		self.assignment = {k:v[0] for k,v in self.variables.items() if len(v)==1 }
		self.arcs = queue()
		self.initializeArcQueue()
		self.enforceArcConsistency()

	def initializeArcQueue(self):
		for var in self.variables:
			neighbors = self.connections(var,self.variables).keys()
			for neighbor in neighbors:
				self.arcs.push((var, neighbor)) 

	def enforceArcConsistency(self):
		while not self.arcs.isEmpty():
			varA, varB = arcs.pop()
			if (varA in self.assignment.keys()) and (len(self.variables[varB]) > 1):
				if self.removeInconsistentValues(varA, varB):
					self.queueArcs(varB)

	def queueArcs(self, var):
		neighbors = connections(var,self.variables).keys()
		for neighbor in neighbors:
			self.arcs.push((var, neighbor))

	def removeInconsistentValues(self, varA, varB):
		assigned = False
		for value in self.variables[varB]:
			if value == self.assignment[varA]:
				self.variables[varB].remove(value)
				if len(self.variables[varB]) == 1: 
					self.assignment[varB] = self.variables[varB][0] #assignment
					assigned = True
		return assigned

	def completed(self):
		return len(self.assignment) == 81

	def selectUnassignedVariable(self, variables, assignment):
		unassigned = [x for x in variables.keys() if x not in assignment]
		return unassigned[0]

	def connections(self, var, nodes):
		row = lambda n: n/9
		col = lambda n: n%9 
		box = lambda n: 3*(row(n)/3)+(col(n)/3)
		return {k:v for k,v in nodes.items() if row(var)==row(k) or col(var)==col(k) or box(var)==box(k)}

	def consistent(self, var, value, assignment):
		return len([x for x in connections(var, assignment).values() if x==value]) == 0

	def backtrackingSearch(self, variables):
		self.enforceArcConsistency()
		return recursiveBacktracking(self.assignment, self.variables)

	def recursiveBacktracking(self, assignment, variables):
		if completed(assignment): return assignment
		var = selectUnassignedVariable(variables, assignment)
		for value in variables[var]:
			if consistent(var, value, assignment):
				assignment[var] = value
				self.queueArcs(var)
				self.enforceArcConsistency()
				result = recursiveBacktracking(assignment, variables)
				if result: return result
				del assignment[var]
		return False		

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

#public
def solve(string):
	sudoku = Game(string)