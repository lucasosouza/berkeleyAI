#failedAttempts.py

initialState = [[x+1 for x in range(9)] for x in range(82)]
fringe = []

def getSuccessors(state):
	#using MRV order - minimum remaining value
	next = []
	index = None
	for idx, var in enumerate(state):
		if len(var) - len(next):
			next = var
			index = idx
	#choose a random subject (will not use LRC for now)
	state[idx] = next[randint(0,len(next)-1)]