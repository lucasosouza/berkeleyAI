"""
function Backtracking-Search(csp) returns solution/failure
	return Recursive-Backtracking({},csp)

function Recursive-Backtracking(assignment,csp) returns solution/failture
	if assignment is complete then return assignment
	var <- Select-Unassigned-Variable(variables[csp], assignment, csp)
	for each value in order-domain-values(var, assignment, csp) do
		if value is consistent with assignment given Constraints[csp] then
			add {var=value to assignment}
			result <- Recursive-Backtracking(assignment,csp)
			if result != failure then return result
			remove {var=value} from assignment
	return failture
"""

#let's implement this in python
# class Problem:
# 	def __init__(self):
#########
#csp = Problem()

def stringToVariables(string):
	nodes = {index:[int(x)] for index, x in enumerate(list(string.replace("-","0")))}
	print {k:[1,2,3,4,5,6,7,8,9] for k,v in nodes.items() if v==0}
	return {k:[1,2,3,4,5,6,7,8,9] for k,v in nodes.items() if v==0}

def selectUnassignedVariable(variables, assignment):
	print "assigned", len(assignment)
	return [x for x in variables.keys() if x not in assignment.keys()][0]

def completed(assignment):
	return len(assignment) == 81
	#return reduce(lambda x,y:x+y, assignment.values()) == 405
	
def connections(var, value, assignment):
	row = lambda n: n/9
	col = lambda n: n%9 
	box = lambda n: 3*(row(n)/3)+(col(n)/3)
	return {k:v for k,v in assignment.items() if row(var)==row(k) or col(var)==col(k) or box(var)==box(k)}

def consistent(var, value, assignment):
	return len([x for x in connections(var, value, assignment).values() if x==value]) == 0

def backtrackingSearch(variables):
	return recursiveBacktracking({},variables)

def recursiveBacktracking(assignment, variables):
	if completed(assignment): return assignment
	var = selectUnassignedVariable(variables, assignment) #, csp)
	for value in variables[var]:
		if consistent(var, value, assignment):
			assignment[var] = value
			result = recursiveBacktracking(assignment, variables)
			if result: return result
			del assignment[var]
	return False		

print backtrackingSearch(stringToVariables('4-5269781682571493197834562826195347374682915951743628519326874248957136763418259'))

