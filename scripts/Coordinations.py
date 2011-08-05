import operator,itertools,numpy

# groups the coordinations by type and lifespan
def GroupCoordinations(data):
	for k,g in itertools.groupby(data):
		g = len(list(g))
		yield (k,g)

def iterCoordinationNames(S,O):
	for i in iterCoordinationNumbers(S,O):
		yield NewCoordinationNumberToName(i)
		
def iterCoordinationNumbers(S,O):
	for s in range(S):
		for o in range(O):
			yield 10*s + o

def CoordinationBins():
	return [100*i + 10*j + k for i in range(3) for j in range(4) for k in range(4)]

def CoordinationNumberToSmallNumber(number):
	# this returns the vanilla S and O values
	return 10*(int(number)/100) + (int(number)%10) + (int(number%100)/10)

def GetCoordinationWeights(trajectories):
	data = reduce(operator.add,trajectories)
	data = map(CoordinationNumberToSmallNumber,data)
	new_bins = [i for i in iterCoordinationNumbers(4,5)]

	histo, edges = numpy.histogram (data, bins=new_bins)

	histo = numpy.array([float(i) for i in histo])
	histo = histo / histo.sum() * 100.0

	edges = map(NewCoordinationNumberToName,edges)
	#print (zip(edges[:-1],histo))
	return dict(zip(edges[:-1],histo))


def CoordinationFilter(t):
  k = t[0].split('-')
  ret = False
  if k[0].count('O') < 4 and k[0].count('S') < 3 and k[1].count('O') < 4 and k[1].count('S') < 3:
  	ret = True
  return ret

def NewCoordinationNumberToName(number):
	name = 'S'*(number/10) + 'O'*(number%10)
	if number == 0:
		name = 'Unbound'
	return name

def CoordinationNumberToName (number):
	number = int(number)
	name = 'S' * (number/100) + 'O' * (number/10%10) + 'O' * (number%10)
	if number == 0:
		name = 'Unbound'
	return name
