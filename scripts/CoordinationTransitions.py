import sys,glob,operator
from ColumnDataFile import ColumnDataFile as CDF

def LoadFiles():
	cdfs_cold = [CDF(f)[0] for f in glob.glob('[1-5]/so2-coordination.dat')]
	cdfs_hot = [CDF(f)[0] for f in glob.glob('[6-9]/so2-coordination.dat')]
	cdfs_hot = cdfs_hot + [CDF(f)[0] for f in glob.glob('10/so2-coordination.dat')]

	return (cdfs_cold,cdfs_hot)

def CoordinationNumberToName (number):
	number = int(number)
	name = 'S' * (number/100) + 'O' * (number/10%10) + 'O' * (number%10)
	if number == 0:
		name = 'Unbound'
	return name

def ParseStateChange(prev,curr,counts):
	prev = CoordinationNumberToName(prev)
	curr = CoordinationNumberToName(curr)
	key = prev+'-'+curr
	if key not in counts:
		counts[key] = 1
	else:
		counts[key] = counts[key] + 1
	return

def PrintStateChanges(counts):
	for k,v in counts.iteritems():
		print k + ' -- ' + str(v)
	return

def PrintStateChangesDOT(counts):
	print "digraph NAME {"

	for k,v in counts.iteritems():
		k = k.split('-')
		if k[0] != k[1]:
			print "\t" + k[0] + " -> " + k[1] + " [ label = " + str(v) + " ];"

	print "}"
	return

def ParseTrajectory(trajectory,counts):
	prev = -1
	for i in trajectory:
		if prev != -1:
			ParseStateChange (prev,i,counts)
		prev = i
	return

def ParseTrajectories(data,counts):
	map(lambda x: ParseTrajectory(x,counts), data)
	return


cold,hot = LoadFiles()
counts = {}
ParseTrajectories(hot,counts)
PrintStateChangesDOT(counts)


	

