import sys,glob,operator,itertools
from ColumnDataFile import ColumnDataFile as CDF
import numpy

def LoadFiles():
	cdfs_cold = [CDF(f)[0] for f in glob.glob('[1-5]/so2-coordination.dat')]
	cdfs_hot = [CDF(f)[0] for f in glob.glob('[6-9]/so2-coordination.dat')]
	cdfs_hot = cdfs_hot + [CDF(f)[0] for f in glob.glob('10/so2-coordination.dat')]

	return (cdfs_cold,cdfs_hot)

def CoordinationBins():
	return [100*i + 10*j + k for i in range(3) for j in range(4) for k in range(4)]

def GetCoordinationWeights(data):
	data = reduce(operator.add,data)
	data = map(CoordinationNumberToNumber,data)
	new_bins = [10*i+j for i in range(3) for j in range(4)]

	histo, edges = numpy.histogram (data, bins=new_bins)

	histo = numpy.array([float(i) for i in histo])
	histo = histo / histo.sum() * 100.0

	edges = map(NewCoordinationNumberToName,edges)
	#print (zip(edges[:-1],histo))
	return dict(zip(edges[:-1],histo))

def NewCoordinationNumberToName(number):
	name = 'S'*(number/10) + 'O'*(number%10)
	if number == 0:
		name = 'Unbound'
	return name

def CoordinationNumberToNumber (number):
	number = int(number)
	number = 10 * (number/100) + (number/10%10) + (number%10)
	return number

def CoordinationNumberToName (number):
	number = int(number)
	name = 'S' * (number/100) + 'O' * (number/10%10) + 'O' * (number%10)
	if number == 0:
		name = 'Unbound'
	return name

def CoordinationNameToNumber (name):
	return 10*name.count('S') + name.count('O')

def ParseStateChange(prev,curr,transitions):
	prev = CoordinationNumberToName(prev)
	curr = CoordinationNumberToName(curr)
	key = prev+'-'+curr
	if key not in transitions:
		transitions[key] = 1
	else:
		transitions[key] = transitions[key] + 1
	return

def PrintStateChanges(transitions):
	for k,v in transitions.iteritems():
		print k + ' -- ' + str(v)
	return

def CoordinationFilter(t):
  k = t[0].split('-')
  ret = False
  if k[0].count('O') < 4 and k[0].count('S') < 3 and k[1].count('O') < 4 and k[1].count('S') < 3:
  	ret = True
  return ret

def PrintStateChangesDOT(transitions):
	vals = [v for k,v in transitions.iteritems() if k.split('-')[0] != k.split('-')[1]]
	max_v = float(max(vals))
	print "digraph NAME { "

	for k,v in itertools.ifilter(CoordinationFilter,transitions.iteritems()):
		k = k.split('-')
		if k[0] == k[1]:
			continue
		arrow = 1.0 + 3.0 * v/max_v	# scale the arrowhead to give a sense of higher traffic
		width = 1.0 + 6.0 * v/max_v
		#label = 12.0 + v/20.0 - 4.0
		print "\t" + k[0] + " -> " + k[1] + " [ label = " + str(v) + ", arrowsize = " + str(arrow) + ", penwidth = " + str(width) + " ];" #", fontsize = " + str(label) + " ];"

	return

def PrintNodeSizes(weights):
	mult = 5.0
	for k,v in weights.iteritems():
		if k.count('O') < 3 and k.count('S') < 3:
			print "\t%s [ width = %f, height = %f];" % (k, v/mult, v/mult)

def ParseTrajectory(trajectory,transitions):
	prev = -1
	for i in trajectory:
		if prev != -1:
			ParseStateChange (prev,i,transitions)
		prev = i
	return

def ParseTrajectories(data,transitions):
	map(lambda x: ParseTrajectory(x,transitions), data)
	return


cold,hot = LoadFiles()
data = cold
transitions = {}
ParseTrajectories(data,transitions)
PrintStateChangesDOT(transitions)

weights = GetCoordinationWeights(data)
PrintNodeSizes(weights)
print "} [ fontsize = 36 ];"

