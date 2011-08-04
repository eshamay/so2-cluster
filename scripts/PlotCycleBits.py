from ColumnDataFile import ColumnDataFile as CDF
import matplotlib.pyplot as plt
from pylab import *
import Smoothing
import sys,numpy,itertools,operator,glob

from scipy import *
import PlotUtility

# groups the signal into 0s and 1s and returns the length of the groups
def CutUpCycleBits(data):
	# now cut up the data into chunks and get their lengths
	for k,g in itertools.groupby(data):
  		# if on then print the cycle life
		if k: yield len(list(g))
  		# if off... print the break life
		#if not k: print len(list(g))

# returns a list with the length of the on or off times of the signal in the given file
def getLifespan(file,axs=None):

	cdf = CDF(file)
	# raw data
	data = cdf[0]

	# smooth out the data and digitize above a certain threshold
	smooth = Smoothing.window_smooth(numpy.array(data), window_len=40, window='blackman')
	smooth = smooth - 0.18
	new_data = numpy.ceil(smooth)

	if axs:
		axs.plot(data, linewidth=2.5, color='k', linestyle=':', alpha=0.7)
		axs.plot(smooth, linewidth=2.0, color='r', linestyle='-', alpha=0.7)
		axs.plot(new_data, linewidth=3.5, color='g', linestyle='-', alpha=0.8)

  	return [c for c in CutUpCycleBits(new_data)]

bns = arange(0,16000,1000)
width=0.35


def PlotCycleBits(files,hot=None):
	lives = [getLifespan(f) for f in files]
	lives = reduce(operator.add,lives)

	total = len(lives)
	histo, edges = numpy.histogram (lives, bins=bns)
	histo = histo * 100.0 / total

	if hot:
		plt.bar([i+width/2 for i in range(len(bns))[:-1]], histo, width, color='r', align='center')
	else:
		plt.bar([i-width/2 for i in range(len(bns))[:-1]], histo, width, color='b', align='center')


fig = plt.figure(num=1, facecolor='w', edgecolor='w', frameon=True)
axs = fig.add_subplot(1,1,1)

files_cold = glob.glob('[1-5]/so2.cyclic-SO-lifespan.dat')

files_hot = glob.glob('[6-9]/so2.cyclic-SO-lifespan.dat')
files_hot = files_hot + glob.glob('10/so2.cyclic-SO-lifespan.dat')

PlotCycleBits(files_cold)
PlotCycleBits(files_hot,True)

xlabel (r'Lifespan of SO$_2$ Cyclic Structure / ps', fontsize=46)
ylabel ('% of SO$_2$ Cyclic Structures', fontsize=46)
xticks (arange(len(bns)), bns/1000, fontsize=32)
yticks (fontsize=42)


plt.show()
