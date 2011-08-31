import sys
import glob
from ColumnDataFile import ColumnDataFile as CDF
import matplotlib.pyplot as plt
from pylab import *
import numpy
import operator
import PlotUtility


def ExtractCoords(files):
  	files = [open(f) for f in files]
  	lines = [f.readline().split() for f in files]
	map(lambda x: x.close(), files)

	data = [numpy.array([int(i) for i in l]) for l in lines]
	data = reduce(operator.add, data)
	return numpy.array(data)

width = 0.35
def PlotBarGraph (files,hot=None):
	data = ExtractCoords(files)
	#total = float(data[0])
	total = 100000.0
	if hot:
		total = 20000.0*4+18238
	cycles = data[2:6]
	#acyclic = (total - data[1])	# time spent acyclic
	cycles = insert(cycles,0,data[1])	# time spent cyclic in the SO coordination
	#cycles = insert(cycles,0,acyclic)
	cycles = append(cycles,data[-2:])	# two types of triple-cycles
	cycles = cycles/total*100.0

	if hot:
		print "hot:"
		print cycles
		plt.bar([i+width/2 for i in range(len(cycles))], cycles, width, color='r', align='center')
	else:
		print "cold:"
		print cycles
		plt.bar([i-width/2 for i in range(len(cycles))], cycles, width, color='b', align='center')
	


#files_cold = glob.glob(sys.argv[1])
files_cold = glob.glob('[1-5]/so2.cyclic-SO.dat')
files_hot = glob.glob('[6-9]/so2.cyclic-SO.dat')
files_hot = files_hot + glob.glob('10/so2.cyclic-SO.dat')

fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
PlotBarGraph (files_cold)
PlotBarGraph (files_hot,True)

xlabel (r'Cycle Type', fontsize=46)
ylabel ('% of Simulated Trajectory', fontsize=46)
names = ['Cyclic', 'Single', 'Double', 'Triple', 'Quadruple', 'Triple-A', 'Triple-B']
xticks (arange(len(names)), names, fontsize=30)
yticks (fontsize=42)

plt.show()

