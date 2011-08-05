import sys,glob,operator,itertools
from ColumnDataFile import ColumnDataFile as CDF
import numpy
import matplotlib
from Coordinations import *
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import matplotlib.pyplot as plt
from pylab import *

def LoadFiles():
	cdfs_cold = [CDF(f)[0] for f in glob.glob('[1-5]/so2-coordination.dat')]
	cdfs_hot = [CDF(f)[0] for f in glob.glob('[6-9]/so2-coordination.dat')]
	cdfs_hot = cdfs_hot + [CDF(f)[0] for f in glob.glob('10/so2-coordination.dat')]

	return (cdfs_cold,cdfs_hot)

def ParseLifespans(trajectories,lifespans):

	for t in trajectories:
		for coord,life in itertools.groupby(t):
			life = len(list(life))
			coord = CoordinationNumberToName(coord)
			if coord not in lifespans:
				lifespans[coord] = []
			lifespans[coord].append(life)

	return

def ParseLifespanStatistics(lifespans):
	# new data where each key is a coordination, and the values are (average, std deviation)
	stats = lifespans.fromkeys(lifespans.keys(), (0.0,0.0))
	for k,v in lifespans.iteritems():
		stats[k] = (numpy.average(v), numpy.std(v))
	return stats

def InitDOTFile():
	print "digraph NAME { "
	return

def PrintDOTNodes(stats):
	averages = operator.getitem(stats.values(),0)
	avg_max = max(averages)
	for k,v in stats.iteritems():
		average = v[0]
		std = v[1]
		print "\t%s [ height=%f, width=%f, fontsize=%d, style=filled, fillcolor=\"0.0,%f,1.0\" ];" % (k, average/10.0, std/10.0, 30, average/avg_max)

	return

def PlotStats(stats,weights,axs):
	patches = []
	for coord,(avg,std) in stats.iteritems():
		circle = Circle((avg, std), weights[coord]*2.0)
		patches.append(circle)
	colors = 100*pylab.rand(len(patches))
	p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.4)
	p.set_array(pylab.array(colors))
	axs.add_collection(p)
	return

def GetData(stats,weights):
	return [(k,weights[k],avg,std) for k,(avg,std) in stats.iteritems()]

def CoordinationLifespanHistograms(lifespans):
	histos = {}
	max_life = max([max(v) for k,v in lifespans.iteritems()])

	for k,v in lifespans.iteritems():
		histo,edges = numpy.histogram (v, bins=arange(0,max_life,100))
		histos[k] = (histo,edges)
	return histos
	

def PlotCoordinationLifespanHistograms(lifespans,axs):
	histos = CoordinationLifespanHistograms(lifespans)

	# max number of S and Os to look at
	S = 2
	O = 3
	patches = []
	for n,c in zip(range((S+1)*(O+1)),iterCoordinationNames(S+1,O+1)):
		#histo,edges = histos[c]
		if c not in lifespans:
			continue
		lives = lifespans[c]
		for l in lives:
		#for h,e in zip(histo,edges):
			#circle = Circle((n,e), h/10.0)
			circle = Circle((n,l), 0.2)
			patches.append(circle)

	#colors = 100*pylab.rand(len(patches))
	p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=0.6)
	#p.set_array(pylab.array(colors))
	axs.add_collection(p)

	return (S+1,O+1)
	
	

cold,hot = LoadFiles()
data = cold
weights = GetCoordinationWeights(data)
lifespans = {}
ParseLifespans(data,lifespans)


fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
axs = fig.add_subplot(111)
s,o = PlotCoordinationLifespanHistograms(lifespans,axs)
bins = [c for c in iterCoordinationNames(s,o)]

xlabel (r'SO$_2$ Coordination', fontsize=46)
ylabel ('Lifespan / fs', fontsize=46)
xticks (arange(len(bins)), bins, fontsize=24)
yticks (fontsize=42)
xlim(-1,12)
ylim(0,3500)
plt.show()
