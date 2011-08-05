import sys,glob,operator,itertools
from ColumnDataFile import ColumnDataFile as CDF
from Coordinations import *
import numpy

def LoadFiles():
	cdfs_cold = [CDF(f)[0] for f in glob.glob('[1-5]/so2-coordination.dat')]
	cdfs_hot = [CDF(f)[0] for f in glob.glob('[6-9]/so2-coordination.dat')]
	cdfs_hot = cdfs_hot + [CDF(f)[0] for f in glob.glob('10/so2-coordination.dat')]

	return (cdfs_cold,cdfs_hot)

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

def PrintStateChangesDOT(transitions):
	vals = [v for k,v in transitions.iteritems() if k.split('-')[0] != k.split('-')[1]]
	max_v = float(max(vals))
	print "digraph NAME { "

	for k,v in itertools.ifilter(CoordinationFilter,transitions.iteritems()):
		k = k.split('-')
		if k[0] == k[1]:
			continue
		width = 0.2 + 15.0 * v/max_v
		print "\t%s -> %s [ label=%d, penwidth=%f, fontsize=%d ];" % (k[0], k[1], v,  width, 36)

	return

def PrintNodeSizes(weights):
  	weight_max = max(weights.values())
	for k,v in weights.iteritems():
		if k.count('O') < 3 and k.count('S') < 3:
			print "\t%s [ width = %f, height = %f, fontsize=30, style=filled, fillcolor = \"0.0,%f,1.0\" ];" % (k, v*5.0/weight_max, v*5.0/weight_max, v/weight_max)

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
print " };"
