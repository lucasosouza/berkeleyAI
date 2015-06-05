
import math

fac = math.factorial
p = 6 #players
win = 27 #integral

def prob(x):
	return float((win**x)*((100-win)**(p-x)))/(100**p)

def comb(x):
	return fac(p)/(fac(x)*fac(p-x))

probs = [(prob(x)*comb(x))for x in range(2,(p+1))]
print 1-(reduce(lambda x, y: x+y, probs))