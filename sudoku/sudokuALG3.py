#arc consistency implementation with backtracking
from sys import stdout
from util import Queue as queue
import copy

def solve(string):
	variables = stringToVariables(string)
	assignment = {k:v[0] for k,v in variables.items() if len(v)==1 }
	prettyPrint(backtrackingSearch(variables, assignment))

def initializeArcQueue(variables):
	arcs = queue()
	for var in variables:
		neighbors = connections(var,variables).keys()
		for neighbor in neighbors:
			arcs.push((var, neighbor))
	return arcs 

def enforceArcConsistency(variables, assignment, arcs):
	while not arcs.isEmpty():
		varA, varB = arcs.pop()
		if (varA in assignment.keys()) and (len(variables[varB]) > 1):
			variables, assignment, assigned = removeInconsistentValues(varA, varB, variables, assignment)
			if assigned:
				arcs = queueArcs(varB, variables, arcs)
	return (assignment, arcs)

def queueArcs(var, variables, arcs):
	neighbors = connections(var,variables).keys()
	for neighbor in neighbors:
		arcs.push((var, neighbor))
	return arcs

def removeInconsistentValues(varA, varB, variables, assignment):
	assigned = False
	for value in variables[varB]:
		if value == assignment[varA]:
			variables[varB].remove(value)
			if len(variables[varB]) == 1: 
				assignment[varB] = variables[varB][0] #assignment
				assigned = True
	return (variables, assignment, assigned)

def completed(assignment):
	return len(assignment) == 81 and reduce(lambda x,y:x+y, assignment.values()) == 405

def selectUnassignedVariable(variables, assignment):
	return [x for x in variables.keys() if x not in assignment][0]

def connections(var, nodes):
	row = lambda n: n/9
	col = lambda n: n%9 
	box = lambda n: 3*(row(n)/3)+(col(n)/3)
	return {k:v for k,v in nodes.items() if row(var)==row(k) or col(var)==col(k) or box(var)==box(k)}

def consistent(var, value, assignment):
	return len([x for x in connections(var, assignment).values() if x==value]) == 0

def backtrackingSearch(variables, assignment):
	arcs = initializeArcQueue(variables)
	enforceArcConsistency(variables, assignment, arcs)
	branchAssignment = copy.deepcopy(assignment)
	return recursiveBacktracking(variables, branchAssignment, assignment, arcs)

def recursiveBacktracking(variables, branchAssignment, assignment, arcs):
	if completed(assignment): return assignment
	var = selectUnassignedVariable(variables, assignment) 
	for value in variables[var]:
		if consistent(var, value, assignment):
			branchAssignment[var] = value
			assignment[var] = value
			arcs = queueArcs(var, variables, arcs)
			branchAssignment, arcs = enforceArcConsistency(copy.deepcopy(variables), branchAssignment, arcs)
			result = recursiveBacktracking(variables, branchAssignment, assignment, arcs)
			if result: return result
			del assignment[var]
	return False		

#end algorithm - start interface
def prettyPrint(assignment):
	i = 0
	for w in range (1,4):
		for x in range(1,4):
			for y in range(1,4):
				stdout.write("|")
				for z in range(1,4):
					stdout.write("%d|" % assignment[i])
					i+=1
				stdout.write(" ")	
			stdout.write("\n")
		stdout.write("-----------------------\n")

def stringToVariables(string):
	nodes = {index:[int(x)] for index, x in enumerate(list(string.replace("-","0")))}
	#nodes = {index:[int(x)] for index, x in enumerate(string)}
	for k,v in nodes.items():
		if v==[0]: nodes[k]=[1,2,3,4,5,6,7,8,9]
	return nodes


""" alternative implementation for selectUnassignedVariable method using MRV and LCV. The minimum remaining value and the least constraining value heuristics seems to select similar unassigned variables on a sudoku problem. Nevertheless, the tests showed on complex boards this heuristic increases the computational time, hence it was abandoned:
def selectUnassignedVariable(variables, assignment):
	unassigned = {k:v for k,v in variables.items() if k not in assignment}
	minimumRemainingValues = max(map(lambda x:len(x), unassigned.values()))
	return [k for k,v in unassigned.items() if len(v)==minimumRemainingValues][0]

note: still need try min-conflicts algorithm 
"""